[![Python package](https://github.com/mrtnbm/Web-Scraper-Public-/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/mrtnbm/Web-Scraper-Public-/actions/workflows/python-package.yml) [![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mrtnbm_Web-Scraper-Public-&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mrtnbm_Web-Scraper-Public-) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/28c3b8b0db3c44cd9dff1739d41ee1b6)](https://www.codacy.com/gh/mrtnbm/Web-Scraper-Public-/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mrtnbm/Web-Scraper-Public-&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/28c3b8b0db3c44cd9dff1739d41ee1b6)](https://www.codacy.com/gh/mrtnbm/Web-Scraper-Public-/dashboard?utm_source=github.com&utm_medium=referral&utm_content=mrtnbm/Web-Scraper-Public-&utm_campaign=Badge_Coverage)
# Numeral-Web-Scraper
Web Scraper for extracting numerals of all languages from languagesandnumbers.com for later analysis. Saves them in a readible .csv format.
## Requirements
- See `requirements.txt`
- Python 3.9+
## Function
Scrapes all numerals listed at [languagesandnumbers.com](https://www.languagesandnumbers.com/) from all 251 languages. Furthermore, the scraped numerals get saved in a CSV-File in the desired script-path which can be viewed in any editor for later analysis. A progress bar indicates how many websites are left.
## Execution
### Binary
- Download the .exe-file from the [releases tab](https://github.com/mrtnbm/Web-Scraper-Public-/releases). Double-click to execute.
### Use/build from Source 
- [Download](https://github.com/mrtnbm/Web-Scraper-Public-/archive/refs/heads/main.zip) and unzip source code or clone the repository with `git clone https://github.com/mrtnbm/Web-Scraper-Public-.git`
- Install Python 3.9+ `sudo apt install python3.9`
- Install requirements `pip install -r requirements.txt` 
- Start script with `python web-scraper-all.py`.
### Build binary yourself
- Execute ```pyinstaller -wF web-scraper-all.py```.
### Run tests
- `python test-web-scraper-all.py`
## GUI
- Main Window for changing settings and selecting a folder to save the csv file  

  ![image](https://user-images.githubusercontent.com/49289399/145732853-98b9c086-eeb3-4257-8568-5a20d9e455b5.png)
- Secondary Window for viewing the progression of the script  

  ![image](https://user-images.githubusercontent.com/49289399/145732832-71deabe4-26da-445e-ba60-669a7f1b6202.png)
## TODO
- Test-Cases for all functions (achieve coverage >= 75%)
- refactor main (more seperate functions, less code in main)
- refactor to meet OOP standards
- fix all code smells
- redirect uploading artifacts to deploy outside of repository
