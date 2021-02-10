from paperscraper.scrapers.base.base_scraper import BaseScraper
import re
"""A scraper of a PMC articles"""


class PMC(BaseScraper):

    def __init__(self, driver):
        self.driver = driver
        self.website = ["ncbi.nlm.nih.gov"]

    def get_authors(self, soup):
        author_links = soup.find("div", {"class": "contrib-group fm-author"}).findAll("a")
        authors = {};

        for i in range(len(author_links)):
            authors['a' + str(i + 1)] = {'last_name': author_links[i].contents[0].split(" ")[-1],
                                         'first_name': author_links[i].contents[0].split(" ")[0]}

        return authors

    def get_abstract(self, soup):

        for heads in soup.find("h2", text=re.compile(r'Abstract')).next_siblings:
            if heads.name == "div":
                abstract = heads.get_text()
                break

        return abstract


        # abstract = soup.find("div", id=lambda x: x and x.startswith('__abstract'))
        # print(abstract)
        # print(soup.find("p", id="__p1"))
        # [tag.unwrap() for tag in abstract.findAll(["em", "i", "b", "sub", "sup"])]
        # return abstract.find("p").contents[0]

    def get_body(self, soup):
        headingNames = [r'Introduction',r'Materials and methods',r'Results',r'Discussion',r'Conclusion']
        text = ""
        for headerName in headingNames:
            for h2 in soup.find("h2", text=re.compile(headerName)).next_siblings:
                if h2.name == "p":
                    text =text + h2.get_text()


        return text


    def get_doi(self, soup):
        return soup.find("span", {"class": "doi"}).find("a").getText()

    def get_keywords(self, soup):
        keywords = soup.find("span", {"class": "kwd-text"})
        [tag.unwrap() for tag in keywords.findAll(["em", "i", "b", "sub", "sup"])]
        return keywords.getText().split(", ")

    def get_pdf_url(self, soup):
        return "https://www.ncbi.nlm.nih.gov/" + soup.find("div", {"class": "format-menu"}).findAll("li")[3].find("a")[
            'href']

    def get_title(self, soup):
        return soup.find("h1", {"class": "content-title"}).getText()
