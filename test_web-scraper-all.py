import unittest

from web_scraper_all import find_lang_short

class test_find_lang_short(unittest.TestCase):
    def test_url_string(self):
        url_data = "https://www.xyz/dcx/ydz/sdsi/german"
        result = find_lang_short(url_data)
        self.assertEqual(result, "german")

if __name__ == '__main__':
    unittest.main()