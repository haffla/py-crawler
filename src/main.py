import math
from src.crawling import Crawling


def pretty_print_dict(dicto, is_dict_in_dict=False):
    for key in sorted(dicto):
        if is_dict_in_dict:
            for k in dicto[key]:
                print("%s: %s" % (key, math.ceil( dicto[key][k] * 10000) / 10000 ))
        else:
            print("%s: %s" % (key, dicto[key]))

if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    crawler = Crawling(base, seed)
    words_dict, urls = crawler.get_links()
    crawler.get_sites_with_links_to_me(1)
    pretty_print_dict(crawler.pageRanks, True)
    pretty_print_dict(words_dict)
