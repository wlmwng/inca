from inca.core.scraper_class import Scraper
import urlexpander
import datetime
import json
import time
from pprint import pprint

import logging
logger = logging.getLogger("INCA")

# TODO: fallback for alt_url (add to retrieve_content)
# TODO: other outlet-specific scrapers
# TODO: custom HTML parse for rushlimbaugh's site
# TODO: use request_archived_url for Washington Examiner


class usmedia(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.doctype = "usmedia"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)

    class NewsContent:
        """
        
        
        """

        def __init__(self, url_info):
            """
            setup the basic NewContent instance
            """
            print("in __init__")
            d = url_info.copy()

            # elasticsearch reference
            self._id = f"{d['outlet']}_{d['url_id']}"

            # add fields from Media Cloud
            self.url_id = d['url_id'] # same as story id
            self.outlet = d['outlet']
            self.publish_date = d['publish_date'] # already converted to UTC
            self.title = d['title']
            self.ap_syndicated = d['ap_syndicated']
            self.themes = d['themes']

            # used for fetching
            self.url = d['url']
            self.alt_url = d['alt_url']

            # hydrated by fetched response
            self.original_url = ''
            self.resolved_url = ''
            self.resolved_domain = ''
            self.resolved_netloc = ''
            self.standardized_url = ''
            self.is_generic_url = ''
            self.response_code = ''
            self.response_reason = ''
            self.fetch_error = ''
            self.FETCH_FUNCTION = ''
            self.FETCH_AT = ''

            # how many secs the retrieval took
            self.TIME_TAKEN = ''

        def retrieve_content(self, url):
            """retrieve the URL's webpage content.
            
            urlexpander.fetch_url():
              1) request with direct server request
              2) if #1 fails, request the URL from the Internet Archive's Wayback Machine if it's available
            
            """
            print("in retrieve")
            # convert 'fetched' from JSON string to dict
            fetched = urlexpander.fetch_url(url)
            fetched = json.loads(fetched)
            self.hydrate(fetched)
            return self

        def hydrate(self, fetched):
            """add fetched content to NewsContent instance"""
            f = fetched.copy()
            self.original_url = f['original_url']
            self.resolved_url = f['resolved_url']
            self.resolved_domain = f['resolved_domain']
            self.resolved_netloc = f['resolved_netloc']
            self.standardized_url = f['standardized_url']
            self.is_generic_url = f['is_generic_url']
            self.response_code = f['response_code']
            self.response_reason = f['response_reason']
            self.fetch_error = f['fetch_error']
            self.FETCH_FUNCTION = f['FETCH_FUNCTION']
            self.FETCH_AT = f['FETCH_AT']

        def json_serializeable(self):
            """Convert values which are not JSON-serializable by default.
            """
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
                    return json.JSONEncoder.default(self, o)

            content = self.__dict__
            as_json = json.dumps(content, cls=CustomEncoder)
            content = json.loads(as_json)
            return content



    def get(self, save, url_info):
        """Document collected via {} scraper""".format(self.doctype)

        print('in get')
        t0 = time.time()
        init = self.NewsContent(url_info=url_info)
        content = init.retrieve_content(url_info['url']) # for washex, try waybackpy in retrieve if maintext is empty and response code is 200
        t1 = time.time()
        content.TIME_TAKEN = t1-t0
        doc = content.json_serializeable()
        yield doc