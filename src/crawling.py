import urllib.request, re, math
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.util.textwrangler import TextWrangler


class Crawling():
    visited = []
    stopwords = []
    url_list = []
    # contains all urls that have no outlinks
    no_outlinks = []
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

    def __init__(self, base_url, seed_list):
        self.url_list = [base_url + site for site in seed_list]
        stopwords_request = urllib.request.urlopen("http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/stop_words.txt")
        stopwords = stopwords_request.read().decode('utf-8')
        stopwords = re.split("\s", stopwords)
        self.stopwords = [re.sub("[,']", "", s) for s in stopwords if s != ""]

    def retrieve_site(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return html

    # TODO: Find better name for this function. What does it do?
    def get_sites_with_links_to_me(self, step):
        start_page_rank = 1 / len(self.url_list)
        for url in self.url_list:
            if step < 1:  # 0 so to say
                # 0.125 for all pages
                self.set_pagerank(url, step, start_page_rank)
            else:
                result = 0
                for inner_url in self.url_list:
                    links_on_page = self.links_dictionary[inner_url]
                    for l in links_on_page:
                        if url == l:
                            previous_pagerank = self.get_pagerank(inner_url, step-1)
                            amount_of_links = len(self.links_dictionary[inner_url])
                            result += previous_pagerank / amount_of_links
                pagerank = self.calculate_pagerank(result, url, step)
                self.set_pagerank(url, step, pagerank)
        if step < 1:
            return 1
        else:
            return self.calc_rank_diff(step)

    def calculate_pagerank(self, sum_of_ego_links, url, step):
        # Implementation of pagerank calculation
        prs_of_no_outlinks = 0
        for outlink in self.no_outlinks:
            prs_of_no_outlinks += self.get_pagerank(outlink, step-1)
        pagerank_result = ((1 - self.damping_factor) / len(self.url_list)) + (self.damping_factor * (sum_of_ego_links + (prs_of_no_outlinks / len(self.url_list))))
        return round(pagerank_result, 4)

    def calc_rank_diff(self, step):
        res = 0
        for key in self.pageRanks:
            curr = self.pageRanks[key][step]
            prev = self.pageRanks[key][step-1]
            res += abs(curr - prev)
        return res

    # puts a pagerank value for a url and a step in pageRanks dictionary
    def set_pagerank(self, url, step, value):
        if url not in self.pageRanks:
            self.pageRanks[url] = {}
        self.pageRanks[url][step] = value

    # return pagerank of url for given step
    # or None if not exists
    def get_pagerank(self, url, step):
        res = self.pageRanks.get(url, None)
        if res is not None:
            res = res.get(step, None)
        return res

    # TODO: Find better name
    def get_links(self):
        for url in self.url_list:
            if url not in self.visited:
                site = self.retrieve_site(url)
                self.visited.append(url)
                soup = BeautifulSoup(site)

                # get text from html document
                text = soup.get_text()
                tokens = TextWrangler.tokenize(text)
                TextWrangler.build_dict(tokens, self.words_dictionary, self.stopwords, url)
                links_on_page = soup.find_all('a')
                if len(links_on_page) == 0:
                    self.no_outlinks.append(url)
                # put every url in links_dictionary and store all links on that particular url
                # thus, we can calculate pageRank later more easily
                # of course concatenating the href with base_url does only work if the href is not a uri itself
                self.links_dictionary[url] = [urllib.parse.urljoin(url, str(a.get('href'))) for a in links_on_page]

                for link in links_on_page:
                    l = urllib.parse.urljoin(url, str(link.get('href')))
                    if l not in self.url_list:
                        self.url_list.append(l)
        return self.words_dictionary, self.url_list