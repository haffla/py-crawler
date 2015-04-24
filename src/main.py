import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/"

sites = ["d01.html", "d06.html", "d08.html"]

url_list = [base_url + site for site in sites]

visited = []

def retrieveSite(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        visited.append(url)
        return html

def getLinksFromSite():
    for url in url_list:
        if url not in visited:
            site = retrieveSite(url)
            soup = BeautifulSoup(site)
            for link in soup.find_all('a'):
                l = urllib.parse.urljoin(url, str(link.get('href')))
                if l not in url_list:
                    url_list.append(l)
                    print(l)

    # just checkin'
    print(len(url_list) == 8)




if __name__ == "__main__":
    getLinksFromSite()