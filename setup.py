from setuptools import setup, find_packages
from paperscraper import __version__, __authors__

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='paperscraper',
    version=__version__,
    license='GNU GENERAL PUBLIC LICENSE',
    description='A web scraping tool to extract the text of scientific papers from journals accessible over university networks.',
    long_description=readme(),
    packages=find_packages(),
    url='https://github.com/NanoNLP/PaperScraper',
    author=__authors__,
    author_email='contact@andriymulyar.com',
    keywords='paperscraper scientific journal web scraper pubmed science-direct acs webscraper',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Science/Research'
    ],
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'requests'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False

)