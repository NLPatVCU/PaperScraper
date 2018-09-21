from unittest import TestCase
from pprint import pprint

from ... import PaperScraper
from collections import OrderedDict

class TestScienceDirect(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = PaperScraper()

    @classmethod
    def tearDownClass(cls):
        cls.scraper.__exit__(None, None, None)



    def test_valid_extraction_1(self):
        scraper = self.scraper
        url = "https://www.sciencedirect.com/science/article/pii/S016635420700469X?via%3Dihub"

        if scraper.is_scrapable(url):
            self.assertIsInstance(scraper.extract_from_url(url), OrderedDict)

    def test_valid_extraction_2(self):
        scraper = self.scraper
        url = "https://www.sciencedirect.com/science/article/pii/S0166093409003346"

        if scraper.is_scrapable(url):
            pprint(dict(scraper.extract_from_url(url)))
            self.assertIsInstance(scraper.extract_from_url(url), OrderedDict)

