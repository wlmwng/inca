import datetime
import logging

from inca.scrapers.usmedia_scraper import usmedia

logger = logging.getLogger("INCA")

class oneamericanews(usmedia):
    """Scrapes oneamericanews"""

    def __init__(self):
        usmedia.__init__(self)  # https://softwareengineering.stackexchange.com/a/318171
        self.doctype = "oneamericanews"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)
