import unittest
import os
os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0.

from unittest.mock import Mock

from web_scraper_all import parse_save_website, write_csv, find_lang_short, find_lang_long

class TestParseSaveWebsite(unittest.TestCase):
    
    def test_parses_website(self):
        # Mock website page response object
        website_page = Mock()
        website_page.content = b'<html><body><a href="how-to-count-in">RandomFirstEntry</a><a href="how-to-count-in-french">French</a></body></html>'
        
        lst_of_links = []
        # Call function with no selected language
        parse_save_website(website_page, lst_of_links)
        
        # Check that lst_of_links contains the expected values
        self.assertEqual(lst_of_links, ['how-to-count-in-french'])
    
    def test_parses_website_with_selected_language(self):
        # Mock website page response object
        website_page = Mock()
        website_page.content = b'<html><body><a href="how-to-count-in-english">English</a><a href="how-to-count-in-french">French</a></body></html>'
        
        lst_of_links = []
        # Call function with selected language
        parse_save_website(website_page, lst_of_links, sel_lang="french")
        
        # Check that lst_of_links contains the expected value
        self.assertEqual(lst_of_links, ['how-to-count-in-french'])
    
    def test_notifies_when_language_not_found(self):
        lst_of_links = []
        # Mock website page response object
        website_page = Mock()
        website_page.content = b'<html><body><a href="how-to-count-in-english">English</a><a href="how-to-count-in-french">French</a></body></html>'
        
        # Call function with selected language not found on website
        with self.assertRaises(SystemExit):
            parse_save_website(website_page, lst_of_links, sel_lang="german")
            
class TestWriteCsv(unittest.TestCase):
    
    def setUp(self):
        self.test_path = '.'
        self.test_string = 'English;1;one\nFrench;1;une\n'
    
    def test_writes_csv_file(self):
        write_csv(self.test_string, self.test_path)
        with open(os.path.join(self.test_path, 'dataset.csv'), 'r', encoding='utf-8-sig') as f:
            contents = f.read()
        self.assertEqual(contents, 'Language;Number;Numeral\n' + self.test_string)
        
    def tearDown(self):
        os.remove(os.path.join(self.test_path, 'dataset.csv'))
        
class test_find_lang_short(unittest.TestCase):
    def test_url_string(self):
        url_data = "https://www.xyz/dcx/ydz/sdsi/german"
        result = find_lang_short(url_data)
        self.assertEqual(result, "german")

class TestFindLangLong(unittest.TestCase):
    
    def test_returns_correct_language(self):
        list_item = 'https://www.example.com/how-to-count-in-english/'
        result = find_lang_long(list_item)
        self.assertEqual(result, 'English')
        
    def test_handles_uppercase_language(self):
        list_item = 'https://www.example.com/how-to-count-in-SPANISH/'
        result = find_lang_long(list_item)
        self.assertEqual(result, 'Spanish')

if __name__ == '__main__':
    unittest.main()