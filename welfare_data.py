from bs4 import BeautifulSoup
import requests
import re
from enum import Enum
from welfare_html_parser import HTMLLoader
from welfare_html_parser import HTMLAdapter
import enum
import datetime

SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
FIRST_YEAR = 2010
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'


class Welfare(enum.Enum):
    cost_of_living = 'cost-of-living'
    crime = 'crime'
    health_care = 'health-care'
    pollution = 'pollution'
    property_investment = 'property-investment'
    quality_of_life = 'quality-of-life'
    traffic = 'traffic'


def log_ranking_to_csv(subject, year):
    URL = MAIN_URL.replace(SUBJECT, subject).replace(YEAR, year)
    html_loader = HTMLLoader(URL, subject, year)
    adapter = HTMLAdapter(html_loader)
    adapter.log_countries_with_headline_to_csv()


def log_all_rankings_to_csvs():
    current_year = int(datetime.datetime.now().year)
    for welfare in Welfare:
        for year in range(FIRST_YEAR, current_year):  # We don't want this current year in the csv because it's not full
            log_ranking_to_csv(welfare.value, str(current_year))


def main():
    log_all_rankings_to_csvs()


if __name__ == '__main__':
    main()
