import requests


class DOIAggregator:
    def __init__(self, driver):
        self.driver = driver

    def extract(self, doi_number, follow_link=True):
        """
        :param doi_number: the doi number of the article link being received
        :param follow_link: default true
        :return: a dictionary with the first link
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

        r = requests.get('https://doi.org/%s' % doi_number, allow_redirects=False)

        return {
            'l0': r.headers['Location']
        }
