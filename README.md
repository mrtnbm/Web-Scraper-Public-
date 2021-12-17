# Numeral-Web-Scraper
Web Scraper for extracting numerals of all languages from languagesandnumbers.com for later analysis. Saves them in a readible .csv format.
## Function
Scrapes all numerals listed at https://www.languagesandnumbers.com/ from all 251 languages. Furthermore, the scraped numerals get saved in a CSV-File in the desired script-path which can be viewed in any editor for later analysis. A progress bar indicates how many websites are left.
## Execution
- Download the .exe-file from the releases tab: https://github.com/mrtnbm/Numeral-Web-Scraper/releases. Double-click to execute. OR
- Unzip source code and start script with `python web-scraper-all.py`. You'll need to download the dependencies `requests` and `bs4`.
- Build .exe with `pyinstaller` yourself: Unzip the archive and execute ```pyinstaller -wF web-scraper-all.py```.
## GUI
- Main Window for changing settings and selecting a folder to save the csv file  

  ![image](https://user-images.githubusercontent.com/49289399/145732853-98b9c086-eeb3-4257-8568-5a20d9e455b5.png)
- Secondary Window for viewing the progression of the script  

  ![image](https://user-images.githubusercontent.com/49289399/145732832-71deabe4-26da-445e-ba60-669a7f1b6202.png)

