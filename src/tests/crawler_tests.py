import unittest
from src.crawling import Crawling


class CrawlerTest(unittest.TestCase):

    def test_dict(self):
        base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
        seed = ["d01.html", "d06.html", "d08.html"]
        crawler = Crawling(base, seed)
        crawler.initialize()

        self.assertEqual(len(crawler.words_dictionary['classification']), 3)
        self.assertEqual(crawler.words_dictionary['classification'][0][0], "d06")
        self.assertTrue(len(crawler.words_dictionary) == 102)


if __name__ == '__main__':
    unittest.main()
