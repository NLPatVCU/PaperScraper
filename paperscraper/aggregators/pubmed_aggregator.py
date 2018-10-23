from bs4 import BeautifulSoup

"""A scientific paper link extractor from by PubMed"""


class PubMedAggregator:
    def __init__(self, driver):
        self.driver = driver

    def extract(self, pubmed_id, follow_link=True):
        """
        :param pubmed_id: pubmed_id of paper that links of will be retrieved.
        :param follow_link: default true
        :return: a dictionary of site url's and journals of the paper associated with pubmed_id structured as
        {
        'l0':{
            'href' = ""
            'journal' = ""
            }

        }
        'l1':{
            'href' = ""
            'journal' = ""
            }

        }
        ...
        """
        if isinstance(pubmed_id, int):
            pubmed_id = str(pubmed_id)
        driver = self.driver
        driver.get("https://www.ncbi.nlm.nih.gov/pubmed/%s" % pubmed_id)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        if soup.find("div", {"class": "icons portlet"}) is None:
            raise IOError("Could not find associated journal links: %s" % pubmed_id)

        a_tags = soup.find("div", {"class": "icons portlet"}).findAll("a", recursive=False)
        links = {}
        for i in range(len(a_tags)):
            links['l' + str(i)] = {}

            if follow_link:
                driver.get(a_tags[i]['href'])
                links['l' + str(i)]['href'] = driver.current_url
            else:
                links['l' + str(i)]['href'] = a_tags[i]['href']

            links['l' + str(i)]['journal'] = a_tags[i]['journal']

        return links
