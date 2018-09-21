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

        author_tags = soup.findAll('meta', {'name': 'citation_author'})
        authors = {}

        for i in range(len(author_tags)):
            author_name = unicodedata.normalize('NFKD', author_tags[i]['content'])
            authors['a' + str(i+1)] = {'last_name': author_name.split(" ")[-1],
                                       'first_name': author_name.split(" ")[0]}

        return authors


    def get_abstract(self, soup):
        return soup.find('p', {'class': 'abstract'}).getText()


    def get_body(self, soup):

        body = OrderedDict()
        # Stop at these sections because no relevant content.
        stop_words = ['Notes and references', 'Acknowledgements', 'Conflicts of interest', 'References']

        # If there are sections iterate through the webpage and use section names as keys to paragraphs
        if soup.find('h2') and not(soup.find('h2').getText() in stop_words):
            counter = 1
            for section in soup.find('p', {'class': 'abstract'}).next_siblings:
                if section.name == 'h2':
                    if section.getText() in stop_words:
                        break
                    body[section.getText()], counter = self.__get_body_helper(section, counter)
        # There are no sections so just return all relevant text under a "no_section" heading
        else:
            paragraphs = OrderedDict()
            counter = 1
            for sibling in soup.find('p', {'class': 'abstract'}).next_siblings:
                if sibling.name == 'p' or sibling.name == 'span':
                    [tag.unwrap() for tag in sibling.findAll(re.compile('^(?!(a|em|i)$).*$'))]
                    paragraphs['p' + str(counter)] = ''.join(str(element) for element in sibling.contents)
                    counter += 1

            body['no_section'] = paragraphs

        return body

    # Helper function called when an article has sections/subsections, recursively parses the text for a section as well as for its subsections
    def __get_body_helper(self, section, counter):
        body = OrderedDict()
        iter_siblings = iter(section.next_siblings)
        for sibling in iter_siblings:
            if sibling.name == 'p' or sibling.name == 'span':
                [tag.unwrap() for tag in sibling.findAll(re.compile('^(?!(a|em|i)$).*$'))]
                body['p' + str(counter)] = ''.join(str(element) for element in sibling.contents)
                counter += 1
            if sibling.name == 'h3':
                if section.name == 'h3':
                    break
                body[sibling.getText()], counter = self.__get_body_helper(sibling, counter)
                # Skip over tags already parsed when collecting subsections
                while(True):
                    parsed_tag = next(iter_siblings, None).next_sibling
                    if parsed_tag == None or parsed_tag.name == 'h3' or parsed_tag.name == 'h2':
                        break
            if sibling.name == 'h2':
                break
        return (body, counter)

    def get_doi(self, soup):
        return soup.find('meta', {'name': 'citation_doi'})['content']


    """ Used to get the keywords from the article

        There are no keywords provided for RSC Articles. Still looking for equivalent.
        """
    def get_keywords(self, soup):
        pass


    def get_pdf_url(self, soup):
        return soup.find('a', {'title': 'Link to PDF version'})['href']


    def get_title(self, soup):
        return soup.find('meta', {'name': 'citation_title'})['content']
