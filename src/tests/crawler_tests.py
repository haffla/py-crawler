import unittest
from src.crawling import Crawling

class CrawlerTest(unittest.TestCase):

    def test_dict(self):
        base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
        seed = ["d01.html", "d06.html", "d08.html"]
        dicto, urls = Crawling(base, seed).get_links()

        self.assertEqual(len(dicto['classification']), 3)
        self.assertTrue(urls[dicto['classification'][0][0]].endswith("d06.html"))
        self.assertTrue(len(dicto) == 102)


if __name__ == '__main__':
    unittest.main()
