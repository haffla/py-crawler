import unittest
from src.crawling import Crawling

class CrawlerTest(unittest.TestCase):

    def test_dict(self):
        base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
        seed = ["d01.html", "d06.html", "d08.html"]
        dicto, urls = Crawling(base, seed).get_links()

        self.assertEqual(len(dicto['classification']), 3)
        self.assertEqual(urls[dicto['classification'][0][0]], 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html')


if __name__ == '__main__':
    unittest.main()
