"""
.. module:: paperscraper
   :synopsis: A class to facilitate the management of multiple scrapers for journal aggregators and publishing sites

.. moduleauthor:: Andriy Mulyar <contact@andriymulyar.com>
"""
from paperscraper.aggregators.doi_aggregator import DOIAggregator
from .aggregators.pubmed_aggregator import PubMedAggregator
from .scrapers.science_direct_scraper import ScienceDirect
from .scrapers.acs_scraper import ACS
from .scrapers.pmc_scraper import PMC
from .scrapers.rsc_scraper import RSC
from selenium import webdriver
import pkg_resources


class PaperScraper():
    """This class provides a direct interface to the inner functionality of paperscraper

    .. note::

       This is the only class needed to utilize all features of paperscraper.

    """

    def __init__(self, webdriver_path=None):
        """Creates a PaperScraper object

        Initializes a PaperScraper that can scrape text and meta-data from scientific journals. Individual journal
        scrapers and journal link aggregators are implemented in :mod:'scrapers' and :mod:'aggregators'.

        :param webdriver_path: The file path of a custom web driver to utilize, defaults to utilize the chromedriver
            that comes installed with the package.
        :type webdriver_path: str.

        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        webdriver_path = pkg_resources.resource_filename('paperscraper', 'webdrivers/chromedriver')

        if ('webdriver_path' is not None):
            self.webdriver_path = webdriver_path

        self.driver = webdriver.Chrome(webdriver_path, options=options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def __import_all_scrapers(self):
        return [ScienceDirect(self.driver), ACS(self.driver), PMC(self.driver), RSC(self.driver)]

    def get_scrapable_websites(self):
        """
        Retrieves all journal urls that are available to be scraped.
        :return:
        """
        return [website for scraper in self.__import_all_scrapers() for website in scraper.website]

    def is_scrapable(self, url):
        """
        Checks if a given url is scrapable by PaperScraper

        :param url: a url containing a full text that needs scrapping
        :return: the Scraper that can scrape url or None
        """

        for website_scraper in self.__import_all_scrapers():
            if (website_scraper.is_correct_url(url)):
                return website_scraper
        return None

    def extract_from_url(self, url):
        """
           Return a JSON file containing a the full text and meta data of the paper located at 'url'.
           Returns None if 'url' cannot be scraped.
           """
        for website_scraper in self.__import_all_scrapers():
            if (website_scraper.is_correct_url(url)):
                return website_scraper.extract(url)
        return None

    def extract_from_pmid(self, pmid):
        """
        Attempts to retrieve a paper given its PMID

        :param pmid:
        :return: An OrderedDict object containing the extracted paper
        """
        pm = PubMedAggregator(self.driver)
        all_sites = pm.extract(pmid)
        for url in [all_sites.get(key)['href'] for key in all_sites.keys()]:
            website_scraper = self.is_scrapable(url)
            if website_scraper is not None:
                return self.extract_from_url(url)

        return None

    def get_sites_from_pmid(self, pmid):
        pm = PubMedAggregator(self.driver)
        all_sites = pm.extract(pmid, follow_link=True)
        return [all_sites.get(key)['href'] for key in all_sites.keys()]

    def get_sites_from_doi(self, doi_num):
        dm = DOIAggregator()
        extracted_site = dm.extract(doi_num)
        return [extracted_site]
