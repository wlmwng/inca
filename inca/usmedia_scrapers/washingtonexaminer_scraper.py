import datetime
import json
import logging
import time

import urlexpander
from inca.scrapers.usmedia_scraper import usmedia

logger = logging.getLogger("INCA")

class washingtonexaminer(usmedia):
    """Scrapes washingtonexaminer"""

    def __init__(self):
        usmedia.__init__(self)  # https://softwareengineering.stackexchange.com/a/318171
        self.doctype = "washingtonexaminer"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)


    def patch_retrieved(self, content):
        """Custom patch for retrieved content.

        Explanation:
            Sample showed that Washington Examiner sometimes returns a 'successful' fetch
            (i.e., response code is 200, 'fetch_error' is False) even if the specific 
            webpage is not found and instead returns a redirected "tag" page.
            
            Example:
            'original_url' is http://www.washingtonexaminer.com/
                            former-sheriff-joe-arpaio-welcomes-but-isnt-asking-for-trump-pardon/article/2631121
            'resolved_url' is https://www.washingtonexaminer.com/tag/donald-trump?
                            source=%2Fformer-sheriff-joe-arpaio-welcomes-but-isnt-asking-for-trump-pardon
                            %2Farticle%2F2631121

            The 'resolved_text' (i.e., HTML) of the response shows:
            <!DOCTYPE html>
            <html class="TagPage" lang="en" itemscope itemtype="http://schema.org/WebPage"><head><meta charset="UTF-8">
            ...

            Since these are false negatives where 'fetch_error' should actually be True,
            this function manually executes step 2 in urlexpander.fetch_url();
            i.e., to request the URL from the Internet Archive's Wayback Machine.

        Args:
            content (NewsContent instance defined in usmedia_scraper)

        Returns:
            patched_content (NewsContent updated to fetch content from archive)

        """
    
        patched_content = content

        f = urlexpander.request_archived_url(patched_content.url)
        fetched = json.loads(f)

        patched_content.hydrate(fetched)
        patched_content.RETRIEVAL_MSG = f"patched retrieval"
        return patched_content


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
        
        if '<html class="TagPage"' in content.resolved_text:
            logger.info(f"'Successful' retrieval was a redirect to a TagPage. Patch the retrieval by requesting the archive.")
            content = self.patch_retrieved(content)
        t1 = time.time()
        content.TIME_TAKEN = t1-t0
        content.resolved_text = ""
        doc = content.json_serializeable()

        yield doc
