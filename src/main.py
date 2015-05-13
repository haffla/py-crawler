import math
from src.crawling import Crawling


def pretty_print_dict(dicto):
    for key in sorted(dicto):
        print("%s: %s" % (key, dicto[key]))

if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    crawler = Crawling(base, seed)
    words_dict, urls = crawler.get_links()
    step = 0
    delta = 0.04
    while crawler.get_sites_with_links_to_me(step) >= delta:
        step += 1
    pretty_print_dict(crawler.pageRanks)
