import urllib.request
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class Tokenizer:

    def tokenize(self, text):
        words = re.split('\W+', text)
        return words






base_url = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"

sites = ["d01.html", "d06.html", "d08.html"]

url_list = [base_url + site for site in sites]

visited = []

dictionary = {}

def retrieveSite(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        visited.append(url)
        return html

def getLinksFromSite():
    i = 0
    for url in url_list:
        if url not in visited:
            site = retrieveSite(url)
            soup = BeautifulSoup(site)

            # get text from html document
            text = soup.get_text()

            #tokenize text
            #normalized_tokens = [token.lower() for token in tokenizer.tokenize(text)][1:-1]

            tokens = tokenizer.tokenize(text)

            for t in tokens:
                if(t not in dictionary):
                    dictionary[t] = [i]
                else:
                    if(i not in dictionary[t]):
                        dictionary[t].append(i)

            for link in soup.find_all('a'):
                l = urllib.parse.urljoin(url, str(link.get('href')))
                if l not in url_list:
                    url_list.append(l)

            i = i + 1


    print(dictionary)


if __name__ == "__main__":
    tokenizer = Tokenizer()
    getLinksFromSite()
