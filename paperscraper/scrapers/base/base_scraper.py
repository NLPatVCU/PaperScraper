from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
"""An abstract wrapper for a scientific paper website scraper"""

class BaseScraper(ABC):

    """
    Should pass through Selenium webdriver instance with your browser of preference
    """
    def __init__(self,driver):
        self.driver = driver


    def extract(self, url):
        """
        A method to handle the extraction of data.
        Returns a dictionary with keys corresponding to various components of a scientific paper.
        """

        if (not self.is_correct_url(url)):
            raise ValueError("Not a %s article: %s" % (", ".join(self.website), url))

        driver = self.driver
        driver.get(url)
        time.sleep(1) # a delay to allow for the loading of paper and all javascript resources
        #TODO test for error in retrieving url
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        return OrderedDict({
            'title':self.get_title(soup),
            'authors': self.get_authors(soup),
            'keywords': self.get_keywords(soup),
            'abstract': self.get_abstract(soup),
            'body': self.get_body(soup),
            'doi':self.get_doi(soup),
            'pdf_url':self.get_pdf_url(soup)
        })

    def is_correct_url(self,url):
        for site in self.website:
            if site in url:
                return True
        return False

    @abstractmethod
    def get_authors(self, soup):
        """
            Returns an OrderedDict of authors structured as
                a1 : {
                    first_name : fname,
                    last_name : lname
                },
                a2 : {
                    first_name : fname,
                    last_name : lname
                }

            Notice, a1 should be first author.
        """
        pass


    @abstractmethod
    def get_body(self, soup):
        """
            Returns a OrderedDict of sections structured as
                section1 : {
                    p1 : contents,
                    p2 : contents,
                    ...
                    pn : contents
                },
                section2 : {
                    p1 : contents,
                    p2 : contents,
                    ...
                    pn : contents
                }

        Paragraphs that do not belong to a section should be placed in a section named 'no_section'.
        See the implementation in ScienceDirect.py for an example.
        """
        pass


    @abstractmethod
    def get_abstract(self,soup):
        """
            Returns the abstract of the paper with its respective paragraphs formatted as:
            {
                p1: contents
                p2: contents
                ...

            }

        """
        pass



    @abstractmethod
    def get_doi(self, soup):
        """
        Returns a string representation of paper DOI or None if non-existant
        """
        pass


    @abstractmethod
    def get_title(self, soup):
        """
        Returns a string representation of paper title
        """
        pass


    @abstractmethod
    def get_pdf_url(self, soup):
        """
        Returns a string representation of url to PDF version of paper or None if non-existant
        """
        pass


    @abstractmethod
    def get_keywords(self, soup):
        """
        Returns an array of keywords associated with a paper or None if non-existent
        """
        pass

