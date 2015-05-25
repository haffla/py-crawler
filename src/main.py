from src.crawling import Crawling
from src.scoring import Scoring
from src.util.pretty_print import Printer

if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    crawler = Crawling(base, seed)
    step = 0
    delta = 0.04
    while crawler.do_page_ranking(step) >= delta:
        step += 1
    #Printer.print_words(crawler.words_dictionary)
    #Printer.print_link_structure(crawler.links_dictionary)
    scorer = Scoring(crawler.words_dictionary, crawler.url_list)
    Printer.print_scoring(scorer.scores)
