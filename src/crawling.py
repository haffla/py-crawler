import urllib.request, re
import requests
import math
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler


class Crawling():
    visited = []
    stopwords = []
    dictionary = {}
    damping_factor = 0.95

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

    def get_ego_links(self, url_list):
        for site in url_list:
            amount_of_all_links = len(url_list)
            start_page_rank = 1 / amount_of_all_links
            base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
            result = 0
            url = site

            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)

            for link in soup.find_all('a'):
                link_to_me = link.get('href')

                crawl_me = base + link_to_me
                sc = requests.get(crawl_me)
                sc_plain_text = sc.text
                ego_soup = BeautifulSoup(sc_plain_text)
                amount_of_links = len(ego_soup.find_all('a'))
                result = result + start_page_rank / amount_of_links
            self.calculate_pagerank(result, url_list, site)

    def calculate_pagerank(self, sum_of_ego_links, url_list, site):
        # (1 - t / N) +  d * (( sum ( ofAllPagesThatHasALinkOfPage01 / AmountOfLinks ) + sum ( ofAllPagesThatHasNoLinkOfPage01 / N ) ) )
        pagerank_result = ((1 - self.damping_factor) / len(url_list)) + (self.damping_factor * ((sum_of_ego_links) + (0.1250 / 8)) )



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

                TextWrangler.build_dict(tokens, self.dictionary, self.stopwords, i)

                for link in soup.find_all('a'):
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)

                i += 1
                # end of for loop over url_list
        self.get_ego_links(self.url_list)
        return self.dictionary, self.url_list