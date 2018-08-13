from paperscraper.scrapers.base.base_scraper import BaseScraper
from collections import OrderedDict


class Springer(BaseScraper):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["link.springer.com"]

    def get_authors(self, soup):
        authors_list = soup.findAll("meta", {"name": "citation_author"})
        return [author['content'] for author in authors_list]

    def get_abstract(self, soup):
        return soup.find("section", {'class': 'Abstract'}).p.getText()

    def get_body(self, soup):
        sections = OrderedDict()
        sections_markup = soup.find("div", id="body").findAll('section', {'class':'Section1'})
        for section_markup in sections_markup:
            paragraphs = section_markup.div.findAll("p", {'class':'Para'})
            sections[section_markup.h2.getText()] = [paragraph.getText() for paragraph in paragraphs]
        return sections

    def get_doi(self, soup):
        return soup.find('meta', {"name": "citation_doi"})['content']

    def get_keywords(self, soup):
        keywords = soup.find('div', {"class": "KeywordGroup"}).findAll('span', {"class": "Keyword"})
        return [keyword.getText() for keyword in keywords]

    def get_pdf_url(self, soup):
        return soup.find('meta', {"name": "citation_pdf_url"})['content']

    def get_title(self, soup):
        return soup.find("meta", {"name": "citation_title"})['content']
