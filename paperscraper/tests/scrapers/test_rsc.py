from unittest import TestCase
from pprint import pprint

from ... import PaperScraper
from collections import OrderedDict

class TestRSC(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = PaperScraper()

    @classmethod
    def tearDownClass(cls):
        cls.scraper.__exit__(None, None, None)

    def test_valid_extraction_1(self):
        scraper = self.scraper
        url = "http://pubs.rsc.org/en/content/articlehtml/2017/CC/C7CC04465H"

        if scraper.is_scrapable(url):
            pprint(dict(scraper.extract_from_url(url)))
            self.assertIsInstance(scraper.extract_from_url(url), OrderedDict)

    def test_valid_extraction_2(self):
        scraper = self.scraper
        url = "http://pubs.rsc.org/en/content/articlehtml/2017/cc/c7cc04949h"

        if scraper.is_scrapable(url):
            pprint(scraper.extract_from_url(url))
            self.assertIsInstance(scraper.extract_from_url(url), OrderedDict)

    def test_invalid_extraction_1(self):
        scraper = self.scraper
        self.assertIsNone(scraper.extract_from_url("google.com"))

    def test_result_contains_authors(self):
        scraper = self.scraper
        result = scraper.extract_from_url("http://pubs.rsc.org/en/content/articlehtml/2017/CC/C7CC04465H")
        self.assertIsNot(result['authors'], {})

    def test_result_contains_body(self):
        scraper = self.scraper
        result = scraper.extract_from_url("http://pubs.rsc.org/en/content/articlehtml/2017/CC/C7CC04465H")
        self.assertIsNot(result['body'], {})