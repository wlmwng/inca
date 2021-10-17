import datetime
import logging

from inca.scrapers.usmedia_scraper import usmedia

logger = logging.getLogger("INCA")

class vdare(usmedia):
    """Scrapes vdare"""

    def __init__(self):
        usmedia.__init__(self)  # https://softwareengineering.stackexchange.com/a/318171
        self.doctype = "vdare"
        self.version = ".1"
        self.date = datetime.datetime(year=2021, month=10, day=6)
