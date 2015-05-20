from src.crawling import Crawling
from src.scoring import Scoring
import math


def pretty_print_dict(dicto):
    for key in sorted(dicto):
        print("%s: %s" % (key, dicto[key]))

if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    crawler = Crawling(base, seed)
    step = 0
    delta = 0.04
    while crawler.do_page_ranking(step) >= delta:
        step += 1
    # pretty_print_dict(crawler.pageRanks)
    # print(self.links_dictionary) # TODO muss noch richtig ausgegeben werden wie auf: http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/link_structure.txt
    scorer = Scoring(crawler.words_dictionary, crawler.url_list) # TODO muss das sein wie?: http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/index.txt

    pretty_print_dict(scorer.doc_lengths)


    #pretty_print_dict(crawler.words_dictionary)