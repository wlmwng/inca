import datetime
from lxml.html import fromstring
from core.scraper_class import Scraper
from scrapers.rss_scraper import rss
from core.database import check_exists
import feedparser
import re
import logging

logger = logging.getLogger(__name__)

def polish(textstring):
    #This function polishes the full text of the articles - it separated the lead from the rest by ||| and separates paragraphs and subtitles by ||.
    lines = textstring.strip().split('\n')
    lead = lines[0].strip()
    rest = '||'.join( [l.strip() for l in lines[1:] if l.strip()] )
    if rest: result = lead + ' ||| ' + rest
    else: result = lead
    return result.strip()

class nieuwsblad(rss):
    """Scrapes nieuwsblad.be"""

    def __init__(self,database=True):
        self.database=database
        self.doctype = "nieuwsblad (www)"
        self.rss_url='http://feeds.nieuwsblad.be/nieuws/snelnieuws'
        self.version = ".1"
        self.date    = datetime.datetime(year=2016, month=8, day=2)

    def parsehtml(self,htmlsource):
        '''
        Parses the html source to retrieve info that is not in the RSS-keys
        In particular, it extracts the following keys (which should be available in most online news:
        section    sth. like economy, sports, ...
        text        the plain text of the article
        byline      the author, e.g. "Bob Smith"
        byline_source   sth like ANP

# html source link
        '''
        try:
            tree = fromstring(htmlsource)
        except:
            print("kon dit niet parsen",type(doc),len(doc))
            print(doc)
            return("","","", "")
# category
        try:
            category = tree.xpath('//*[@class="is-active"]/text()')[0]
        except:
            category=""
# teaser
        try:
            teaser = tree.xpath('//article//div//div//P/text()')
        except:
            teaser =""
# text
        try:
            text = tree.xpath('//article//div//p/text()')
        except:
            text =""

# author
        try:
            author = tree.xpath('//article//footer/p/span/text()')[0]
        except:
            author =""

        extractedinfo={"category":category.strip(),
                       "teaser":teaser,
                       "byline":author.split(),
                       "text":text.split()
                       }

        return extractedinfo
