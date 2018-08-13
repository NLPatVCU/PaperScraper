from paperscraper.scrapers.base.base_scraper import BaseScraper
"""A scraper for The Royal Society of Chemistry (RSC) articles"""


class RCS(BaseScraper):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["pubs.rsc.org"]

    def get_authors(self, soup):
        return soup.find("meta", {"name": "citation_author"})['content']

    def get_abstract(self, soup):
        return soup.find("p", {'class': 'abstract'}).getText()

    def get_body(self, soup):
        pass

    def get_doi(self, soup):
        return soup.find("meta", {"name": "citation_doi"})['content']

    """ Used to get the keywords from the article

        There are no keywords provided for RSC Articles. Still looking for equivalent.
        """
    def get_keywords(self, soup):
        pass

    def get_pdf_url(self, soup):
        return soup.find('a', {"title": "Link to PDF version"})['href']

    def get_title(self, soup):
        return soup.find("meta", {"name": "citation_title"})['content']
