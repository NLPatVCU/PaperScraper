
PaperScraper
============
PaperScraper facilitates the extraction of text and meta-data from scientific journal articles for use in NLP systems.
In simplest application, query by the URL of a journal article and receive back a structured JSON object containing the article text and metadata.
More robustly, query by relevant attribute tags of articles (ie. DOI, Pubmed ID) and have an article URL automatically found and extracted from.

![alt text](https://nlp.cs.vcu.edu/images/Edit_NanomedicineDatabase.png "Nanoinformatics")

Use
===
Retrieve structured journal articles in three lines:
```python
from paperscraper import PaperScraper
scraper = PaperScraper()
print(scraper.extract_from_url("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3418173/"))
```
```
{
  "title": "Gentamicin-loaded nanoparticles show improved antimicrobial effects towards Pseudomonas aeruginosa infection"
  "abstract": "...",
  "body": "...",
  "authors": {
    "a1": {"first_name": "Sharif", "last_name": "Abdelghany"},
    "a2": {"first_name": "Derek", "last_name": "Quinn"},
    "a3": {"first_name": "Rebecca", "last_name": "Ingram"},
    "a4": {"first_name": "Brendan", "last_name": "Gilmore"},
    "a5": {"first_name": "Ryan", "last_name": "Donnelly"},
    "a6": {"first_name": "Clifford", "last_name": "Taggart"},
    "a7": {"first_name": "Christopher", "last_name": "Scott"}
  },
  "doi": "10.2147/IJN.S34341",
  "keywords": [
    "anti-microbial",
    "gentamicin",
    "PLGA nanoparticles",
    "Pseudomonas aeruginosa"
  ],
  "pdf_url": "https://www.ncbi.nlm.nih.gov//pmc/articles/PMC3418173/pdf/ijn-7-4053.pdf"
}
```
or use a domain-specific aggregator such as PubMed and let PaperScraper automatically find a link for you:
```python
from paperscraper import PaperScraper
scraper = PaperScraper()
print(scraper.extract_from_pmid("22915848"))
```

Current Scraping Capabilities
=============================
Journal | Scraper |
--- | --- |
Science Direct | :heavy_check_mark: |
Pubmed Central (PMC) | :heavy_multiplication_x: |
Springer | :heavy_check_mark: |
American Chemical Society (ACS) | :heavy_multiplication_x: |
Royal Society of Chemistry (RSC) | :heavy_check_mark: |

Contribution
============
To contribute an additional scraper to PaperScraper simply do the following (detailed instructions found in section 'Example Contribution Development Set-up'):

1. Fork this repository and clone down a local version of your fork.
2. set-up/enter a virtual environment using a Python version of 3.5 or greater.
3. Run the setup.py file and verify that all package requirements have successfully installed in your virtual environment.
4. Contribute a scraper by adding a file to the [paperscraper/scrapers](paperscraper/scrapers) directory following the naming convention '\<journal\>_scraper.py'. Your scraper should implement the BaseScraper interface and simply include the necessary methods (see other scrapers for examples). The package will handle all other integration of your scraper into the framework.
5. PaperScraper utilizes BeautifulSoup4 for navigating markdown. When writing a scraper, each method receives an instance of a BeautifulSoup object that wraps the markdown of the queried website. This markdown is then navigated to retrieve relevant information. See [BeautifulSoup documentation and examples](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
6. While developing a scraper, one should simultaneously be write a test file under [tests/scrapers](tests/scrapers) named 'test_\<journal\>.py' . This will not only allow the concurrent debugging of each method as one develops, but more importantly allow for the identifications of any markdown changes (and resulting scraping errors) the publisher makes after development concludes. We emphasis, **writing a test is vital** to the longevity of your contribution and subsequently the package. See 'Detailed Contribution Instructions' for a walk-through of testing a contribution.
7. Once complete, run all package tests with nosetests and submit a pull request.

Contribution Standards
======================
Follow the following formatting standards when developing a scraper:

1. Include all meta-html tags inside of the body such as links (\<a\>), emphasis \<em\>, etc. These can be filtered out by the end user but can also serve to provide meaningful information to some systems.
2. The OrderedDict containing the paper body should be structured as follows:
```
{
  "body": {
    "Name of section": {
        "Name of nested section": {
            "p1": "The raw text of first paragraph"
        }
        "p2": "raw text of second paragraph"
    },
    "p3":"Raw text of third paragraph",
    "p4":"Raw text of fourth paragraph"

  }
}
```

Example Contribution Development Set-up
=======================================
We recommend using an IDE such as PyCharm to facilitate the contribution process. It is available
for [free](https://www.jetbrains.com/student) if you are affiliated with a university . This contribution walk-through assumes that you are utilizing PyCharm Professional Edition.

1. Create a new PyCharm project named 'PaperScraper'. When selecting an interpreter, click the gear icon and create a new virtual environment (venv) in a version of Python greater than 3.5  ([details here](https://www.jetbrains.com/help/pycharm-edu/creating-virtual-environment.html)). A Python virtual environment serves to isolate your current development from all python packages and version already installed on your machine.
2. Fork this repository, navigate to the directory of your project, and clone your fork into it.
3. The PyCharm directory view should now update with all relevant project files. Press the button 'Terminal' in the lower-left corner of the IDE to open up an in-IDE terminal instance local to your project - notice the virtual environment is already set.
4. Execute `python setup.py` to install PaperScraper and its dependencies into your virtual environment.
5. Execute `python setup.py test` to run all tests. Insure that you have an internet connection as some tests require it. Further tests (along with only running single test files) can be executed by the command 'nosetests' ([details here](http://nose.readthedocs.io/en/latest/usage.html#selecting-tests)).
6. Create new files '\<journal\>\_scraper.py' and 'test\_\<journal\>.py' in [paperscraper/scrapers](paperscraper/scrapers) and [tests/scrapers](tests/scrapers) respectively. Model the structure/naming conventions of these files after other files in the directories.
7. When testing your contribution-in-progress, run the command 'nosetesting -s \<test_file_path\>' to test only a single file. The '-s' parameter will allow print statements in your test files to show when tests are run. These should be removed before making a pull request.


Testing
=======================================
Ensure that you have an internet connection before testing.
To execute all tests, run the command `python setup.py test` from the top-level directory.  
To execute a single test, run the command `nosetests -s <test_file_path>`.  The -s flag will allow print statements to print to console.  Please remove all print statements before submitting a pull request.

Check out the Nose testing documentation [here](https://nose.readthedocs.io/en/latest/testing.html).  

If you are experiencing errors running tests, make sure Nose is running with a version of python 3.5 or greater.
If it is not, it is likely an error with Nose not being installed in your virtual environment.  Execute the command `pip install nose -I` to correctly install it.  

When writing tests, cover scraping from a few different correct and incorrect URLs.  Also test that there is valid output
for key sections such as 'authors' and 'body'.  **Please follow the naming convention for your test files**.  Refer to the test_sciencedirect.py file as a template for your own tests.

License
=======
This package is licensed under the GNU General Public License

Acknowledgments
===============
- [VCU Natural Language Processing Lab](https://nlp.cs.vcu.edu/)     ![alt text](https://nlp.cs.vcu.edu/images/vcu_head_logo "VCU")
- [Nanoinformatics Vertically Integrated Projects](https://rampages.us/nanoinformatics/)
