"""

prnt-scraper.py

A simple scraper for prnt.sc

Features:
Downloads images automatically from found links
Rotating proxies from IP:PORT list



"""


import random
import string
import argparse
import requests
from pathlib import Path

parser = argparse.ArgumentParser(description="A simple scraper for prnt.sc")

parser.add_argument("--number", help="The number of URLs to try", default=10, type=int)
parser.add_argument("--output", help="Output path for images", default="./", type=str)
parser.add_argument("--proxies", help="Path to proxies file, formatted IP:PORT")

args = parser.parse_args()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0 Safari/537.36"
    )
}

proxy_list = []

# check that output directory exists
output_path = Path(args.output)
output_path.mkdir(parents=True, exist_ok=True)


def generate_random_string(length=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def download_image_from_url(img_name: str, img_url_data):
    if img_url_data != -1:
        print(f"Image found, downloading {img_name}.png")
        with open(output_path / f"{img_name}.png", "wb") as f:
            f.write(img_url_data)


def find_image_name_in_response(response: str):
    start, end = "https://image.prntscr.com/image/", ".png"
    i1 = response.find(start)
    i2 = response[i1:].find(end) + i1 + len(end) # regex too scary for me
    if i1 != -1 and i2 != -1:
        return response[i1 + len(start):i2 - len(end)]
    return -1


def import_proxies_from_file(filename):
    global proxy_list
    with open(filename, "r") as f:
        proxy_list = [line.strip() for line in f if line.strip()]


def scrape_url(url: str):
    if proxy_list:
        # tries a different random proxy, found more success with this method
        random.shuffle(proxy_list)
        for proxy in proxy_list:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            try:
                response = requests.get(f"https://prnt.sc/{url}", headers=headers, proxies=proxies, timeout=8)
                if response.status_code == 200:
                    img_name = find_image_name_in_response(response.text)
                    if img_name != -1:
                        img_url = f"https://image.prntscr.com/image/{img_name}.png"
                        download_image_from_url(img_name, requests.get(img_url, headers=headers, proxies=proxies).content or -1)
                    break
            except Exception as e:
                print(f"Proxy {proxy} failed: {e}")
    else:
        try:
            response = requests.get(f"https://prnt.sc/{url}", headers=headers, timeout=8)
            if response.status_code == 200:
                img_name = find_image_name_in_response(response.text)
                if img_name != -1:
                    img_url = f"https://image.prntscr.com/image/{img_name}.png"
                    download_image_from_url(img_name, requests.get(img_url, headers=headers).content or -1)
        except Exception as e:
            print(f"Request failed: {e}")


def main():
    global proxy_list
    urls = [generate_random_string().lower() for _ in range(args.number)]
    if args.proxies:
        import_proxies_from_file(args.proxies)

    for url in urls:
        scrape_url(url)


if __name__ == "__main__":
    main()
