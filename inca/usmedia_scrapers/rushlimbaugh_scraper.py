import datetime
import logging
import time

from bs4 import BeautifulSoup
from inca.scrapers.usmedia_scraper import usmedia

logger = logging.getLogger("INCA")

class rushlimbaugh(usmedia):
    """Scrapes rushlimbaugh"""

    def __init__(self):
        usmedia.__init__(self)  # https://softwareengineering.stackexchange.com/a/318171
        self.doctype = "rushlimbaugh"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)

    def parse_html(self, html):
        """custom parser because newsplease (in super class) can't parse content from rushlimbaugh
        Args:
            html (str): HTML string
        
        Returns:
            parsed (str): article text
        """

        try:
            text_list = []
            content_div = BeautifulSoup(html, features="lxml").find("div", {"class": "entry-content"})
            for p in content_div.find_all("p"):
                text_list.append(p.get_text().strip())
            text_list = [x for x in text_list if x != ""]
            text = " ".join(text_list)
            parsed = text
        except TypeError:
            parsed = ""
        except AttributeError: # AttributeError("'NoneType' object has no attribute 'find_all'")
            parsed = ""
        return parsed


    def patch_retrieved(self, content):
        """Fix article_maintext and update related attrs"""

        patched_content = content
        patched_content.article_maintext = self.parse_html(patched_content.resolved_text)
        patched_content.article_maintext_is_empty = False if len(patched_content.article_maintext) > 0 else True
        patched_content.RETRIEVAL_MSG = f"patched retrieval"
        return patched_content


    def get(self, save, url_info):
        """
        Args:
            save (bool): required by INCA's internal logic for setting up scrapers
            url_info (dict): see NewsContent's __init__ for required keys

        Yields:
            doc
        """
        t0 = time.time()
        init = self.NewsContent(url_info=url_info)
        content = init.retrieve_content()
        
        # a sample showed that news-please fails to extract the article maintext of rushlimbaugh URLs
        if content.article_maintext_is_empty:
            content = self.patch_retrieved(content)
        t1 = time.time()
        content.TIME_TAKEN = t1-t0
        content.resolved_text = ""
        doc = content.json_serializeable()

        yield doc
