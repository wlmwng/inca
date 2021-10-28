"""
This file contains the twitter API retrieval classes
"""

import datetime
import json
import logging

from requests import HTTPError
from twarc import Twarc2, expansions

from ..core.basic_utils import dotkeys
from ..core.client_class import Client, elasticsearch_required
from ..core.search_utils import doctype_first

logger = logging.getLogger(f"INCA.{__name__}")


class twitter2(Client):
    """Class defined mainly to add credentials

    The twitter2 client uses app-auth through an OAuth-2.0 Bearer Token.
    Access is read-only.
    The rate limits on Twitter through app-auth (instead of user-auth) are generally higher.

    """

    service_name = "twitter2"

    @elasticsearch_required
    def add_application(self, appname="default"):
        """Add a twitter2 app to generate credentials"""

        app_prompt = {
            "header": "Add twitter2 application",
            "description": "Twitter API v2 (Academic Product Track): \n"
            "https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research",
            "inputs": [
                {
                    "label": "Application name",
                    "description": "Name for internal use",
                    "help": "Just a string to denote the application within INCA",
                    "input_type": "text",
                    "mimimum": 4,
                    "maximum": 15,
                    "default": appname,
                },
                {
                    "label": "User ID",
                    "description": "User ID on Twitter",
                    "help": "Just a string to denote the associated User ID with the application within INCA",
                    "input_type": "text",
                    "mimimum": 4,
                    "maximum": 15,
                    "default": appname,
                },
                {
                    "label": "Bearer token",
                    "description": "Copy-paste the code shown in the 'Bearer Token' field (OAuth 2.0)",
                    "help": "Go to the developer portal (https://developer.twitter.com/en/portal/dashboard). \n"
                    "Select your application and navigate to the 'Keys and tokens' tab.",
                    "input_type": "text",
                    "mimimum": 8,
                },
            ],
        }
        response = self.prompt(app_prompt, verify=True)
        return self.store_application(
            app_credentials={
                "user_id": response["User ID"],
                "bearer_token": response["Bearer token"],
            },
            appname=response["Application name"],
        )

    @elasticsearch_required
    def add_credentials(self, appname="default"):
        """Required by parent class (see core/client_class).
        Retrieve the appropriate app credentials with
        `self.load_application`, create a credentials dictionary
        and store them by calling the `self.store_credentials` method.

        Original purpose is to retrieve consumer keys/tokens as part of 3-legged authentication.
        Twitter API v2 using bearer token does not require this step, so just return credentials as-is.
        """

        logger.info(f"Adding credentials to {appname}")
        application = self.load_application(app=appname)
        credentials = dotkeys(application, "_source.credentials")

        return self.store_credentials(
            app=appname,
            credentials=json.dumps(credentials),
            id=credentials["user_id"],
        )

    def _get_client(self, credentials):
        if type(credentials) == str:
            credentials = json.loads(credentials)
        return Twarc2(bearer_token=credentials["bearer_token"])

    def _set_delay(self, *args, **kwargs):
        """Twarc handles rate limiting"""
        pass


class twitter2_timeline(twitter2):
    """Class to retrieve twitter timelines for a given account

    Use the full-archive search endpoint instead of
    the user_timeline endpoint which returns the most recent 3,200 tweets only.
    Ref: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/3-deciding-which-endpoints-to-use.md

    "If you want more than 3200 recent Tweets authored by a user,
    you can use the full-archive search endpoint and specify the
    username in your query using the from: operator
    e.g. from:TwitterDev and specify the time period for older Tweets."
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all)

    """

    def get(
        self,
        credentials,
        screen_name,
        force=False,
        since_id=None,
        until_id=None,
        start_time=datetime.datetime.now(datetime.timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        - datetime.timedelta(days=7),
        end_time=datetime.datetime.now(datetime.timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ),
    ):
        """get account timeline from Twitter API v2 search endpoint"""

        self.doctype = "tweets2"
        self.version = "0.1"
        self.functiontype = "twitter2_client"
        self.date = datetime.datetime(2021, 8, 21, 0, 0, 0, 0, datetime.timezone.utc)

        api = self._get_client(credentials=dotkeys(credentials, "_source.credentials"))

        if not force:

            # The purpose of setting 'since_id' is to conserve API resources.
            # Only new tweets which did not exist at the time of previous retrieval will be collected.
            # If 'since_id' is not set, then the API will return all tweets by the account;
            # i.e., the response will return all tweets, even if they had already been collected by INCA.

            # 'since_id': tweets older than this id will not be included in the response.
            # 'doctype_first': the oldest doc in INCA corresponds with the most recent tweet in INCA.

            # Example:
            # INCA collects an account's tweets on June 15, 2020.
            # At this time, the account contains T1 (posted on May 1), T2 (May 15), and T3 (May 31).
            # INCA stores each tweet as a doc in ES (doc['_source']).
            # T3, T2, and T1 are stored by INCA in that order.
            # As a result, doctype_first(...) will return the id of T3 (most recent tweet, oldest doc)
            # rather than the id of T1 (oldest tweet, newest doc).

            # The account adds two tweets after June 15, 2020.
            # At this time, the timeline contains T1, T2, T3, T4 (June 17), and T5 (June 20).
            # doctype_first(...) sets 'since_id' to the id of T3.
            # As a result, only tweets posted after T3 (i.e., T5 and T4) are included in the response.
            # doctype_first(...) will then set 'since_id' to the id of T5 in a future retrieval.

            # 'until_id' is set to None (similar to max_id in Twitter API v1.1)
            # The Twitter API v2 provides it for pagination purposes,
            # but no value is needed since twarc already handles pagination (and rate limiting).

            # References:
            # https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/guides/working-with-timelines
            # https://stackoverflow.com/questions/6412188/what-exactly-does-since-id-and-max-id-mean-in-the-twitter-api

            since_id = doctype_first(
                doctype="tweets2", query="author.username:" + screen_name
            )
            if len(since_id) == 0:
                logger.info(
                    "settings since_id to None as there are no tweets for this user"
                )
                since_id = None
            else:
                since_id = since_id[0].get("_source", {}).get("id", None)
                logger.info(f"settings since_id to {since_id}")
        try:
            # the search_all method calls the full-archive search endpoint
            # and returns a paginated generator
            response = api.search_all(
                query=f"from:{screen_name}",
                since_id=since_id,
                until_id=until_id,
                start_time=start_time,
                end_time=end_time,
                max_results=100,
            )

            # collect the hydrated tweets returned by the endpoint
            # hydration is done on a page-by-page basis
            # (https://twarc-project.readthedocs.io/en/latest/api/expansions/)
            tweets = []
            for page in response:
                hydrated_tweets = expansions.flatten(page)
                for tweet in hydrated_tweets:
                    tweets.append(tweet)

            for num, tweet in enumerate(tweets):
                if self._check_exists(tweet["id"])[0] and not force:
                    logger.info(f"skipping existing {screen_name}-{tweet['id']}")
                    continue
                tweet["_id"] = tweet["id"]
                if not (num + 1) % 100:
                    logger.info(
                        f"retrieved {num} tweets for {screen_name} with tweet_id = {tweet['_id']}"
                    )

                yield tweet

        except HTTPError as err:
            logger.error(
                f"HTTP status code {err.response.status_code}: {err.response.text}"
            )

        except Exception as err:
            logger.error(f"Unhandled exception: {err}")
