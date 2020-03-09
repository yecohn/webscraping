from bs4 import BeautifulSoup
import requests
import re
from enum import Enum


class HAPPINESS(Enum):
    COST_OF_LIVING = 1
    CRIME = 3
    CLIMATE = 4
    FOOD_PRICES = 5
    GAS_PRICES = 6
    HEALTH_CARE = 7
    POLLUTION = 8
    PROPERTY_INVESTMENT = 9
    QUALITY_OF_LIFE = 10
    TAXI_FARE = 11
    TRAFFIC = 12


MAIN_URL = 'https://www.numbeo.com/cost-of-living/'


def get_raw_data():
    return requests.get(MAIN_URL).text


def get_all_urls(raw_data):
    soup = BeautifulSoup(raw_data, 'html.parser')
    return [element.get('value') for element in soup.findAll('option', attrs={"value": re.compile('https.+')})]


def navigate_to_subject_according_to_user():
    raw_data = get_raw_data()
    main_urls = get_all_urls(raw_data)

    print(main_urls)


def main():
    navigate_to_subject_according_to_user()


if __name__ == '__main__':
    main()
