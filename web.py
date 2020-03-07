from bs4 import BeautifulSoup
import requests
import urllib.request
import time

URL = 'https://www.numbeo.com/cost-of-living/'


def get_data_from_URL(url):
    return requests.get(url)


def parse_response(response):
    return BeautifulSoup(response.text, 'html.parser')


def manage_public_welfare():
    response = get_data_from_URL(URL)
    data = parse_response(response)
    print(data)


def main():
    manage_public_welfare()


if __name__ == '__main__':
    main()
