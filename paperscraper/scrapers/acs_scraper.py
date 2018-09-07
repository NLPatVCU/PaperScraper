import re

from paperscraper.scrapers.base.base_scraper import BaseScraper

"""A scraper for American Chemical Society (ACS) articles"""


class ACS(BaseScraper):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["pubs.acs.org"]

    def get_authors(self, soup):
        author_links = soup.find("div", id="articleMeta").findAll("a", id="authors")
        authors = {}

        for i in range(len(author_links)):
            authors['a' + str(i + 1)] = {'last_name': author_links[i].contents[0].split(" ")[-1],
                                         'first_name': author_links[i].contents[0].split(" ")[0]}

        return authors

    def get_abstract(self, soup):
        return soup.find("p", {'class': 'articleBody_abstractText'}).getText()

    def get_body(self, soup):

        body = []

        def is_reference(tag):
            prev_neg = False
            if tag.previous_sibling:
                prev_neg = "-" == tag.previous_sibling.string
            is_ion = "+" in tag.getText()
            is_anion = "-" in tag.getText() or prev_neg
            return tag.name == "sup" and not (is_ion or is_anion)

        # Take out the references, tables, and figures
        [s.extract() for s in soup.find_all(is_reference)]
        [s.extract() for s in soup.find_all("table")]
        [s.extract() for s in soup.find_all({'class': "figure"})]

        article_sections = soup.find_all("div", class_='NLM_sec')

        for section in article_sections:

            sectionTitle = section.find('h2')

            if sectionTitle:
                sectionTitle = section.find('h2').get_text()
            else:
                sectionTitle = "NO SECTION HEADER PROVIDED"

            paragraphs = section.find_all("div", class_="NLM_p")

            for i, paragraph in enumerate(paragraphs):
                paragraph_text = paragraph.get_text()
                body.append({"text": paragraph_text, "meta": {"section": sectionTitle, "paragraph": i + 1}})

        return body

    def get_doi(self, soup):
        doi_block = soup.find("div", id="doi")
        doi_block.next_element.extract()
        return doi_block.getText()

    """ Used to get the keywords from the article
    
    There are no keywords provided for ACS Articles. Still looking for equivalent.
    """

    def get_keywords(self, soup):
        pass

    def get_pdf_url(self, soup):
        return "https://pubs.acs.org" + \
               soup.find(
                   "ul", {"class": "publicationFormatList icons"}
               ).find(
                   "li", {'class': 'pdf-low-res'}
               ).find("a")['href']

    def get_title(self, soup):
        return soup.find("span", {"class": "hlFld-Title"}).getText()
