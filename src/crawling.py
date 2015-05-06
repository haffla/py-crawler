import urllib.request, re
import math
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler


class Crawling():
    visited = []
    stopwords = []
    words_dictionary = {}
    links_dictionary = {}
    damping_factor = 0.95
    base_url = ""

    def __init__(self, base_url, seed_list):
        self.base_url = base_url
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

    def get_ego_links(self, url_list):
        start_page_rank = 1 / len(url_list)
        for url in url_list:
            result = 0
            for page in self.links_dictionary[url]:
                # TODO: Check if links shows to me (ex: d01.html == d01.html? goToSiteAndCheckNumberOfLinks : Ignore)
                amount_of_links = len(self.links_dictionary[self.base_url + page])
                result += start_page_rank / amount_of_links
            self.calculate_pagerank(result, url)


    def calculate_pagerank(self, sum_of_ego_links, site):
        # (1 - t / N) +  d * (( sum ( ofAllPagesThatHasALinkOfPage01 / AmountOfLinks ) + sum ( ofAllPagesThatHasNoLinkOfPage01 / N ) ) )
        pagerank_result = ((1 - self.damping_factor) / len(self.url_list)) + (self.damping_factor * ((sum_of_ego_links) + (0.1250 / 8)) )
        print(site, math.ceil( pagerank_result * 10000) / 10000 )

    def get_links(self):
        i = 0
        for url in self.url_list:
            if url not in self.visited:
                site = self.retrieve_site(url)
                soup = BeautifulSoup(site)

                # get text from html document
                text = soup.get_text()

                tokens = TextWrangler.tokenize(text)

                TextWrangler.build_dict(tokens, self.words_dictionary, self.stopwords, i)

                links_on_page = soup.find_all('a')
                # put every url in links_dictionary and store all links on that particular url
                # thus, we can calculate pageRank later more easily
                self.links_dictionary[url] = [str(a.get('href')) for a in links_on_page]

                for link in links_on_page:
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)

                i += 1
                # end of for loop over url_list
        self.get_ego_links(self.url_list)
        return self.words_dictionary, self.url_list
