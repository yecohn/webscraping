from bs4 import BeautifulSoup
from enum import Enum
from welfare_html_parser import HTMLLoader
from welfare_html_parser import HTMLAdapter
import datetime
import logging
import settings
import sys


class WelfareType(Enum):
    cost_of_living = 'cost-of-living'
    crime = 'crime'
    health_care = 'health-care'
    pollution = 'pollution'
    property_investment = 'property-investment'
    quality_of_life = 'quality-of-life'
    traffic = 'traffic'


class WelfareManager:

    def __init__(self):
        self.logger = logging.getLogger(settings.LOGGER_NAME)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))  # adds print to console

    def log_ranking_to_csv(self, subject, year):
        html_loader = HTMLLoader(subject, year)
        adapter = HTMLAdapter(html_loader)
        adapter.log_countries_with_headline_to_csv()

    def log_all_rankings_to_csvs(self):
        current_year = int(datetime.datetime.now().year)
        for welfare_type in WelfareType:
            for year in range(settings.FIRST_YEAR, current_year):
                # We don't want current_year outputted to the user because that data of the current year isn't full
                self.log_ranking_to_csv(welfare_type.value, str(year))


def main():
    welfareManager = WelfareManager()
    welfareManager.log_all_rankings_to_csvs()


if __name__ == '__main__':
    main()
