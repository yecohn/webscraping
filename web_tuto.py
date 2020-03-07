from bs4 import BeautifulSoup
import requests
import urllib
import time

URL = 'https://www.numbeo.com/cost-of-living/'


def get_data_from_URL(url):
    return requests.get(URL)


def parse_response(response):
    return BeautifulSoup(response.text, 'data.html')


def main():
    response = get_data_from_URL(URL)
    data = parse_response(response)


if __name__ == '__main__':
    main()
