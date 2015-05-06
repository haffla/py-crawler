from src.crawling import Crawling

if __name__ == "__main__":
    base = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"
    seed = ["d01.html", "d06.html", "d08.html"]
    dicto, urls = Crawling(base, seed).get_links()
    print(len(dicto))
    print(urls)
