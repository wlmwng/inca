import datetime
import json
import logging
import time
import numpy as np

import requests
import urlexpander
from inca.core.scraper_class import Scraper

logger = logging.getLogger("INCA")


class usmedia(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.doctype = "usmedia"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)

    class NewsContent:
        """
        Instances of the NewsContent class are filled out by the scrapers for various outlets
        located in the usmedia_scrapers directory.

        __init__:           setup the template with the input URL's information.
                            the prepopulated attrs are based on the externally prepared input.
        retrieve_content:   use the 'url' and 'alt_url' to retrieve the article.
        hydrate:            fill out the remaining attrs based on the retrieved content.
        json_serializeable: prep the content to produce a document ready to be stored in Elasticsearch.
        get:                required by INCA's internal logic to make the scraper available publicly.

        """

        def __init__(self, url_info):
            """
            setup the basic NewContent instance
            """
            d = url_info

            # project reference
            self.PROJECT = "usmedia"
            self._id = f"{d['outlet'].replace(' ', '')}_{d['url_id']}"

            # add fields from Media Cloud
            self.url_id = d["url_id"]  # same as story id
            self.outlet = d["outlet"]
            self.publish_date = d["publish_date"]  # already converted to UTC
            self.title = d["title"]
            self.ap_syndicated = d["ap_syndicated"]
            self.themes = d["themes"]

            # used for fetching
            self.url = d["url"]
            self.alt_url = d["alt_url"]

            # hydrated by fetched response
            # dummy values are necessary because Elasticsearch mapping expects certain types
            # RequestError: RequestError(400, 'mapper_parsing_exception',
            # "failed to parse field [FETCH_AT] of type [date] in document with id 'dailycaller_567'")
            self.article_maintext = ""
            self.article_maintext_is_empty = True  # for Kibana
            self.original_url = ""
            self.resolved_url = ""
            self.resolved_domain = ""
            self.resolved_netloc = ""
            self.standardized_url = ""
            self.is_generic_url = False
            self.response_code = -1
            self.response_reason = ""
            self.fetch_error = True
            self.FETCH_FUNCTION = "Fetch failed to start"
            self.FETCH_AT = "1900-01-01T00:00:00.000000"

            # how many secs it took to create the doc
            self.TIME_TAKEN = ""
            self.RETRIEVAL_MSG = ""

            # since HTML is lengthy, put it at the end of the obj for readability
            self.resolved_text = ""

        def retrieve_content(self):
            """retrieve the URL's webpage content.

            Try to fetch with 'self.url' first. If it fails, try to fetch with 'self.alt_url'.

            urlexpander.fetch_url():
              1) request with direct server request
              2) if #1 fails, request the URL from the Internet Archive's Wayback Machine if it's available
            """
            logger.info(f"retrieving url_id {self.url_id}, url: {self.url}")

            try:
                f1 = urlexpander.fetch_url(self.url)
                f1 = json.loads(f1)
                fetched = f1

                f1_error = f1["fetch_error"]  # bool
                self.RETRIEVAL_MSG = f"fetch_error (url): {f1_error}"

                logger.info(f"completed retrieval with primary URL")

            except requests.exceptions.RequestException as e:
                # https://docs.python-requests.org/en/master/_modules/requests/exceptions/
                # e.g., InvalidSchema, MissingSchema, InvalidURL
                # https://stackoverflow.com/a/16511493
                f1_error = True
                self.RETRIEVAL_MSG = f"fetch_error (url): {f1_error}, {str(e)}"

            except Exception as e:
                # just in case (can troubleshoot specifics in ES/Kibana)
                f1_error = True
                self.RETRIEVAL_MSG = f"fetch_error (url): {f1_error}, {str(e)}"

            if f1_error:
                logger.info(
                    f"failed to retrieve with primary URL, trying alternative URL"
                )

                try:
                    f2 = urlexpander.fetch_url(self.alt_url)
                    f2 = json.loads(f2)
                    fetched = f2

                    f2_error = f2["fetch_error"]
                    self.RETRIEVAL_MSG = f"fetch_error (alt_url): {f2_error}"
                    logger.info(f"completed retrieval with alternative URL")

                except requests.exceptions.RequestException as e:
                    f2_error = True
                    self.RETRIEVAL_MSG = f"fetch_error (alt_url): {f2_error}, {str(e)}"

                except Exception as e:
                    f2_error = True
                    self.RETRIEVAL_MSG = f"fetch_error (alt_url): {f2_error}, {str(e)}"

            try:
                self.hydrate(fetched)

            except UnboundLocalError as e:
                logger.warning(
                    f"Failed to retrieve url_id {self.url_id} with url {self.url} and alt_url {self.alt_url}"
                )
            return self

        def hydrate(self, fetched):
            """update the NewsContent instance with the fetched info"""
            f = fetched
            self.article_maintext = (
                "" if f["article_maintext"] is None else f["article_maintext"]
            )
            self.article_maintext_is_empty = (
                False if len(self.article_maintext) > 0 else True
            )
            self.original_url = f["original_url"]
            self.resolved_url = f["resolved_url"]
            self.resolved_domain = f["resolved_domain"]
            self.resolved_netloc = f["resolved_netloc"]
            self.standardized_url = f["standardized_url"]
            self.is_generic_url = f["is_generic_url"]
            try:
                self.response_code = (
                    -1 if np.isnan(f["response_code"]) else int(f["response_code"])
                )
            except TypeError:
                # HTTP response codes should be numeric
                # the server didn't return a numeric value
                self.response_code = -1
            self.response_reason = f["response_reason"]
            self.fetch_error = f["fetch_error"]
            self.resolved_text = f["resolved_text"]
            self.FETCH_FUNCTION = f["FETCH_FUNCTION"]
            self.FETCH_AT = f["FETCH_AT"]

        def json_serializeable(self):
            """Convert values which are not JSON-serializable by default"""
            # https://stackoverflow.com/a/27058505
            class CustomEncoder(json.JSONEncoder):
                """
                By default, JSON serializable types are booleans, integers, floating point numbers, and strings.
                CustomEncoder is a subclass of json.JSONEncoder.
                It modifies datetime and dictionary types to make them JSON serializable.
                Modify this subclass to address other non-primitive types.
                """

                def default(self, o):
                    if isinstance(o, datetime.datetime):
                        # https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
                        # Return a string representing the date and time in ISO 8601 format
                        # e.g., '2019-05-18T15:17:00+00:00'
                        return o.isoformat()
                    elif isinstance(o, dict):
                        return json.dumps(o)
                    elif o is None:
                        return ""

                    return json.JSONEncoder.default(self, o)

            content = self.__dict__
            as_json = json.dumps(content, cls=CustomEncoder)
            content = json.loads(as_json)
            return content

    def get(self, save, url_info):
        """
        Args:
            save (bool): required by INCA's scraper setup logic
            url_info (dict): see NewsContent's __init__ for required keys

        Yields:
            doc
        """
        t0 = time.time()
        init = self.NewsContent(url_info=url_info)
        content = init.retrieve_content()
        t1 = time.time()
        content.TIME_TAKEN = t1 - t0
        content.resolved_text = ""
        doc = content.json_serializeable()

        yield doc
