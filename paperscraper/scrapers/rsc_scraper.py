from paperscraper.scrapers.base.base_scraper import BaseScraper
from collections import OrderedDict
import unicodedata
import re

"""A scraper for The Royal Society of Chemistry (RSC) articles"""


class RSC(BaseScraper):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["pubs.rsc.org"]


    def get_authors(self, soup):

        author_tags = soup.findAll("meta", {"name": "citation_author"})
        authors = {}

        for i in range(len(author_tags)):
            author_name = unicodedata.normalize("NFKD", author_tags[i]['content'])
            authors['a' + str(i+1)] = {'last_name': author_name.split(" ")[-1],
                                       'first_name': author_name.split(" ")[0]}

        return authors


    def get_abstract(self, soup):
        return soup.find("p", {'class': 'abstract'}).getText()


    def get_body(self, soup):

        body = OrderedDict()

        # If there are sections iterate through the webpage and use section names as keys to paragraphs
        if soup.find("h2") and soup.find("h2").getText() != "Notes and references":
            for sibling in soup.find("p", {'class': 'abstract'}).next_siblings:
                if sibling.name == "h2":
                    # Stop at these sections because no relevant content
                    if sibling.getText() == "Notes and references" or sibling.getText() == "Acknowledgements":
                        break

                    paragraphs = OrderedDict()
                    counter = 1
                    for tag in sibling.next_siblings:
                        if tag.name == "p" or tag.name == "span":
                            paragraphs['p' + str(counter)] = unicodedata.normalize('NFKD', tag.getText())
                            counter += 1
                        if tag.name == "h2":
                            break
                    body[sibling.getText()] = paragraphs

        # There are no sections so just return all relevant text under a "no_section" heading
        else:
            paragraphs = OrderedDict()
            counter = 1
            for sibling in soup.find("p", {'class': 'abstract'}).next_siblings:
                if sibling.name == "p" or sibling.name == "span":
                    # Stop at these sections because no relevant content.
                    if sibling.getText() == "Notes and references" or sibling.getText() == "Acknowledgements":
                        break
                    [tag.unwrap() for tag in sibling.findAll(re.compile('^(?!(a|em|i|span)$).*$'))]
                    print(sibling.contents)
                    paragraphs['p' + str(counter)] = unicodedata.normalize('NFKD', sibling.getText())
                    counter += 1

            body["no_section"] = paragraphs

        return body


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
