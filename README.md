
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
print(scraper.extract("http://link-to-journal-article.com"))
```

Contribution
============
To contribute an additional scraper to PaperScraper simply do the following (detailed instructions found in section 'Example Contribution Development Set-up'):

1. Clone a local version of this repository and set-up/enter a virtual environment using a Python version of 3.5 or greater.
2. Run the setup.py file and verify that all package requirements have successfully installed in your virtual environment.
3. Contribute a scraper by adding a file to the paperscraper/scrapers directory following the naming convention '\<journal\>_scraper.py'. Your scraper should implement the BaseScraper interface and simply include the necessary methods (see other scrapers for examples). The package will handle all other integration of your scraper into the framework.
4. PaperScraper utilizes BeautifulSoup4 for navigating markdown. When writing a scraper, each method receives an instance of a BeautifulSoup object that wraps the markdown of the queried website. This markdown is then navigated to retrieve relevant information. See [BeautifulSoup documentation and examples](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
5. While developing a scraper, one should simultaneously be write a test file under tests/scrapers named 'test_\<journal\>.py' . This will not only allow the concurrent debugging of each method as one develops, but more importantly allow for the identifications of any markdown changes (and resulting scraping errors) the publisher makes after development concludes. We emphasis, **writing a test is vital** to the longevity of your contribution and subsequently the package. See 'Detailed Contribution Instructions' for a walk-through of testing a contribution.
6. Once complete, run all packages tests and submit a pull request.


Example Contribution Development Set-up
=======================================
We recommend using an IDE such as PyCharm to facilitate the contribution process. It is available
for [free](https://www.jetbrains.com/student) if you are affiliated with a university . This contribution walk-through assumes that you are utilizing PyCharm Professional Edition.

1. Create a new PyCharm project named 'PaperScraper'. When selecting an interpreter, click the gear icon and create a new virtual environment (venv) in a version of Python greater than 3.5  ([details here](https://www.jetbrains.com/help/pycharm-edu/creating-virtual-environment.html)). A Python virtual environment serves to isolate your current development from all python packages and version already installed on your machine.
2. Fork this repository, navigate to the directory of your project, and clone your fork into it.
3. The PyCharm directory view should now update with all relevant project files. Press the button 'Terminal' in the lower-left corner of the IDE to open up an in-IDE terminal instance local to your project - notice the virtual environment is already set.
4. Execute 'python setup.py' to install PaperScraper and its dependencies into your virtual environment.
5. Execute 'python setup.py test' to run all tests. Insure that you have an internet connection as some tests require it. Further tests (along with only running single test files) can be executed by the command 'nosetests' ([details here](http://nose.readthedocs.io/en/latest/usage.html#selecting-tests)).
6. Create new files '\<journal\>\_scraper.py' and 'test\_\<journal\>.py' in [paperscraper/scrapers](paperscraper/scrapers) and [tests/scrapers](tests/scrapers) respectively. Model the structure/naming conventions of these files after other files in the directories.
7. When testing your contribution-in-progress, run the command 'nosetesting -s \<test_file_path\>' to test only a single file. The '-s' parameter will allow print statements in your test files to show when tests are run. These should be removed before making a pull request.

License
=======
This package is licensed under the GNU General Public License

Acknowledgments
===============
- [VCU Natural Language Processing Lab](https://nlp.cs.vcu.edu/)     ![alt text](https://nlp.cs.vcu.edu/images/vcu_head_logo "VCU")
- [Nanoinformatics Vertically Integrated Projects](https://rampages.us/nanoinformatics/)
