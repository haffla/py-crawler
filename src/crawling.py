import urllib.request, re, math
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler
from src.scoring import Scoring


class Crawling():
    visited = []
    stopwords = []
    url_list = []
    # contains all urls that have no outlinks
    no_out_links = []
    # nested dictionaries. for instance: { 'd02': { 1: 0.11, 2: 0.21 } }
    # meaning d02's pagerank for step 1 is 0.11 and for step 2 is 0.21
    pageRanks = {}
    # holds unique normalized words pointing to document where they occur + number of each occurrence
    # for instance: 'classification' => 'each': [('d01', 1), ('d02', 2)]; meaning the word 'each' occurs once
    # in document d01 and twice in document d02.
    words_dictionary = {}
    # holds all links of all sites, for instance: 'd01' => ['d02', 'd03', 'd05']
    links_dictionary = {}
    damping_factor = 0.95
    start_page_rank = 0

    def __init__(self, base_url, seed_list):
        self.url_list = [base_url + site for site in seed_list]
        stopwords_request = urllib.request.urlopen("http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/stop_words.txt")
        stopwords = stopwords_request.read().decode('utf-8')
        stopwords = re.split("\s", stopwords)
        self.stopwords = [re.sub("[,']", "", s) for s in stopwords if s != ""]
        self.initialize()
        self.start_page_rank = 1 / len(self.url_list)

    @staticmethod
    def retrieve_site(url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return html

    def do_page_ranking(self, step):
        for url in self.url_list:
            if step < 1:  # 0 so to say
                self.set_page_rank(url, step, self.start_page_rank)
            else:
                result = 0
                # go through all sites again
                for inner_url in self.url_list:
                    links_on_page = self.links_dictionary[inner_url]
                    # check all links on the site
                    for l in links_on_page:
                        # if it has a link to the current url, sum up pagerank from step before and divide by the amount of links
                        if url == l:
                            previous_page_rank = self.get_page_rank(inner_url, step-1)
                            amount_of_links = len(self.links_dictionary[inner_url])
                            result += previous_page_rank / amount_of_links
                page_rank = self.calculate_page_rank(result, step)
                self.set_page_rank(url, step, page_rank)
        if step < 1:
            return 1
        else:
            return self.calc_rank_diff(step)

    def calculate_page_rank(self, result, step):
        # sum of page_rank of sites that have no outlinks
        prs_without_out_links = 0
        for out_link in self.no_out_links:
            prs_without_out_links += self.get_page_rank(out_link, step-1)
        page_rank_result = ((1 - self.damping_factor) / len(self.url_list)) + \
            (self.damping_factor * (result + (prs_without_out_links / len(self.url_list))))
        return round(page_rank_result, 4)

    def calc_rank_diff(self, step):
        res = 0
        for key in self.pageRanks:
            curr = self.pageRanks[key][step]
            prev = self.pageRanks[key][step-1]
            res += abs(curr - prev)
        return res

    # puts a pagerank value for a url and a step in pageRanks dictionary
    def set_page_rank(self, url, step, value):
        if url not in self.pageRanks:
            self.pageRanks[url] = {}
        self.pageRanks[url][step] = value

    # return pagerank of url for given step
    # or None if not exists
    def get_page_rank(self, url, step):
        res = self.pageRanks.get(url, None)
        if res is not None:
            res = res.get(step, None)
        return res

    # initializes crawling of urls, collection of additional urls, tokenizing, building of word_dictionary..
    def initialize(self):
        for url in self.url_list:
            if url not in self.visited:
                site = self.retrieve_site(url)
                self.visited.append(url)
                soup = BeautifulSoup(site)
                text = soup.get_text()
                tokens = TextWrangler.tokenize(text)
                TextWrangler.build_dict(tokens, self.words_dictionary, self.stopwords, url)
                links_on_page = soup.find_all('a')
                # if the page does not have outlinks we add it to the no_outlinks list
                if len(links_on_page) == 0:
                    self.no_out_links.append(url)
                # put every url in links_dictionary and store all links on that particular url
                # thus, we can calculate pageRank later more easily
                self.links_dictionary[url] = [urllib.parse.urljoin(url, str(a.get('href'))) for a in links_on_page]


                for link in links_on_page:
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)