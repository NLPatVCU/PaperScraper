from unittest import TestCase
from pprint import pprint

from .. import PaperScraper
from selenium import webdriver
from collections import OrderedDict

class TestPaperScraper(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scraper = PaperScraper()
        cls.driver = cls.scraper.driver

    @classmethod
    def tearDownClass(cls):
        cls.scraper.__exit__(None, None, None)


    def test_init(self):
        scraper = self.scraper
        self.assertIsInstance(scraper, PaperScraper)

    def test_driver(self):
        driver = self.driver
        self.assertIsInstance(driver, webdriver.Chrome, msg=
        """
        Driver must be an instance of webdriver.Chrome. Please verify that chromedriver was installed alongside
        PaperScraper; otherwise, set the webdriver_path argument to the location of the chromedriver binary on your 
        machine upon initializing an instance of PaperScraper"
        """)


    def test_valid_extraction(self):
        scraper = self.scraper
        url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/"

        if scraper.is_scrapable(url):
            pprint(dict(scraper.extract_from_url("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/")))
            self.assertIsInstance(scraper.extract_from_url(url), OrderedDict)

    def test_invalid_extraction(self):
        scraper = self.scraper
        self.assertIsNone(scraper.extract_from_url("https://www.google.com"))

