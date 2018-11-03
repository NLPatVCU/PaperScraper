import requests


class DOIAggregator:
    def __init__(self):
        pass

    def extract(self, doi_number, follow_link=True):
        """
        :param doi_number: the doi number of the article link being received
        :param follow_link: default true
        :return: a dictionary with the first link
        {
        'l0': '[link]'
        ...
        """

        r = requests.get('https://doi.org/%s' % doi_number, allow_redirects=False)
        if r.status_code == 404:
            raise ValueError("Could not find a document with that DOI")
        else:
            return {
                'l0': r.headers['Location']
            }
