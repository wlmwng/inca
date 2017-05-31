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

class tijd(rss):
    """Scrapes tijd.nl"""

    def __init__(self,database=True):
        self.database=database
        self.doctype = "ad (www)"
        self.rss_url=['http://www.tijd.be/rss/ondernemen.xml','http://www.tijd.be/rss/politiek.xml','http://www.tijd.be/rss/markten_live.xml','http://www.tijd.be/rss/opinie.xml','http://www.tijd.be/rss/cultuur.xml','http://www.tijd.be/rss/netto.xml','http://www.tijd.be/rss/sabato.xml']
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
        '''
        try:
            tree = fromstring(htmlsource)
        except:
            print("kon dit niet parsen",type(doc),len(doc))
            print(doc)
            return("","","", "")
#author
        try:
             author = tree.xpath('//*[@class="m-meta__item-container"]//a/text()')
        except:
             author = ""
#teaser
        try:
            teaser = tree.xpath('//*[@class="l-main-container-article__intro highlightable "]/text()')
        except:
            teaser = ""
             
#text
        try:
             text = "".join(tree.xpath('//*[@class="l-main-container-article__article"]//div//p/text()'))
        except:
             text =""
           
    
 #category
        try:
            category = tree.xpath('//*[@class="m-breadcrumb__item--last"]/a/span/text()')
        except:
            category =""

        extractedinfo={"byline":author,
                       "text":text.strip(),
                       "category":category,
                       "teaser":teaser
                       }

        return extractedinfo
