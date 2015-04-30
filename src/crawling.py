import urllib.request, re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler


class Crawling():

    visited = []
    stopwords = []
    dictionary = {}

    def __init__(self, base_url, seed_list):
        self.url_list = [base_url + site for site in seed_list]
        stopwords_request = urllib.request.urlopen("http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/stop_words.txt")
        stopwords = stopwords_request.read().decode('utf-8')
        stopwords = re.split("\s", stopwords)
        self.stopwords = [re.sub("[,']", "", s) for s in stopwords if s != ""]

    def retrieve_site(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            self.visited.append(url)
            return html

    def get_links(self):
        i = 0
        for url in self.url_list:
            if url not in self.visited:
                site = self.retrieve_site(url)
                soup = BeautifulSoup(site)

                # get text from html document
                text = soup.get_text()

                tokens = TextWrangler.tokenize(text)

                TextWrangler.build_dict(tokens, self.dictionary, self.stopwords, i)

                for link in soup.find_all('a'):
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)

                i += 1
                # end of for loop over url_list

        return self.dictionary, self.url_list
