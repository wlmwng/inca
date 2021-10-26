import datetime
from lxml.html import fromstring
from inca.core.scraper_class import Scraper
from inca.scrapers.rss_scraper import rss
from inca.core.database import check_exists
import feedparser
import re
import logging

logger = logging.getLogger("INCA")


class stuttgarterzeitungpolitik(rss):
    """Scrapes the politics section of https://www.stuttgarter-zeitung.de/ """

    def __init__(self):
        self.doctype = "stuttgarter zeitung (www)"
        self.rss_url = [
            "https://www.stuttgarter-zeitung.de/politik.rss.feed",
        ]
        self.version = ".1"
        self.date = datetime.datetime(year=2020, month=3, day=19)

    def parsehtml(self, htmlsource):
        """
        Parses the html source to retrieve info that is not in the RSS-keys
        In particular, it extracts the following keys (which should be available in most online news:
        section    sth. like economy, sports, ...
        text        the plain text of the article
        byline      the author, e.g. "Bob Smith"
        byline_source   sth like ANP
        """
        try:
            tree = fromstring(htmlsource)
        except:
            logger.warning("HTML tree cannot be parsed")

        # category
        try:
            category = tree.xpath(
                '//*[@class="brickgroup nav-breadcrumb cf"]/ul/li[1]//text()'
            )
        except:
            category = ""

        # title: consists out of two parts:
        # title1
        try:
            title1 = tree.xpath('//*[@class="mod-header-article"]/h1/em//text()')
        except:
            title1 = ""
        # title2
        try:
            title2 = tree.xpath('//*[@class="mod-header-article"]/h1/strong//text()')
        except:
            title2 = ""
        title = title1 + title2
        # teaser
        try:
            teaser = tree.xpath('//*[@class="box-lead"]//text()')
        except:
            teaser = ""
        # author
        try:
            author = tree.xpath('//*[@class="contentbrick box-author"]/text()')
        except:
            author = ""
        # text
        try:
            text = "".join(tree.xpath('//*[@class="brickgroup mod-article"]//p/text()'))
        except:
            text = ""

        extractedinfo = {
            "category": category,
            "title": title,
            "teaser": teaser,
            "text": text,
            "byline": author,
        }

        return extractedinfo