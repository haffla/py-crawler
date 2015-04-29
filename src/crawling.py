import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler


class Crawling(object):

    visited = []
    dictionary = {}

    def __init__(self, base_url, seed_list):
        self.url_list = [base_url + site for site in seed_list]

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

                TextWrangler.build_dict(tokens, self.dictionary, i)

                for link in soup.find_all('a'):
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)

                i += 1
                # end of for loop over url_list

        return self.dictionary, self.url_list


if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    dicto, urls = Crawling(base, seed).get_links()
    print(dicto)
    print(urls)
