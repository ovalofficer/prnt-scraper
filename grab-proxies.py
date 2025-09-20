"""

grab-proxies.py

Modified version of my Free-Proxy-List-Scraper
https://github.com/ovalofficer/Free-Proxy-List-Scraper

Changes:
Always outputs to 'proxies.txt'
Scrapes only 'anonymous' rated proxies
Grabs 100 proxies at a time


"""

import requests
from bs4 import BeautifulSoup


def get_xml(url: str):
    return BeautifulSoup(requests.get(url).text, 'lxml')


def output_to_file(info: list[str]):
    with open(f"proxies.txt", 'w') as file:
        for e in info:
            file.write(e + "\n")

    print(f"{len(info)} proxies saved to: 'proxies.txt'")


def scrape_freeproxylist():
    info = []

    site = get_xml('https://free-proxy-list.net/en/anonymous-proxy.html')

    proxy_table = site.find_all('table', class_='table table-striped table-bordered')

    for entries in proxy_table:
        entry = entries.find_all('tr')
        for block in entry:
            data = block.find_all('td')
            if data:
                info.append(f"{data[0].text}:{data[1].text}")

                # IP PORT COUNTRYCODE COUNTRY ANONYMITY GOOGLE HTTPS LASTCHECKED
                #  0    1           2       3         4      5     6           7
                # TODO: ADD TOGGLE FUNCTIONALITY TO CHOOSE INFO

    return info


if __name__ == '__main__':
    output_to_file(scrape_freeproxylist())
