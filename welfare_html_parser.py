from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
import settings
import sys

SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'
HTTP_SUCCESS = 200


class HTMLLoader:

    def __init__(self, subject, year):
        self.url = MAIN_URL.replace(SUBJECT, subject).replace(YEAR, year)
        self.subject = subject
        self.year = year
        self.logger = logging.getLogger(settings.LOGGER_NAME)
        self.response_text = None
        self.response_soup = None

    def get_data(self):
        self.response_text = self.fetch_text_from_url()
        self.response_soup = self.parse_response()
        return self.response_soup

    def fetch_text_from_url(self):
        self.logger.info(f'Started fetching data from {self.url}')
        try:
            response = requests.get(self.url)
        except (TypeError, ConnectionError, Exception) as e:
            self.logger.critical(e, exc_info=True)
            exit()
        self.logger.info(f'Finished fetching data from {self.url}')
        if response.status_code != HTTP_SUCCESS:
            self.logger.critical(e, exc_info=True)
            exit()
        return response.text

    def parse_response(self):
        self.logger.info(f'Started parsing response from {self.url}')
        try:
            self.response_soup = BeautifulSoup(self.response_text, 'html.parser')
            self.logger.info(f'Finished parsing response from {self.url}')
            return self.response_soup
        except (TypeError, Exception) as e:
            self.logger.critical(e, exc_info=True)
            exit()


class HTMLAdapter:

    def __init__(self, html_loader):
        self.html_loader = html_loader
        self.logger = logging.getLogger(settings.LOGGER_NAME)

    def get_countries_titles(self):
        tags = self.html_loader.response_soup.find_all('th')
        return [tag.get_text() for tag in tags]

    def get_countries(self):
        countries_result = []
        countries_html = self.html_loader.response_soup.find_all('tr', style="width: 100%")
        [countries_result.append(country.text) for country in countries_html]
        countries = [item.split('\n') for item in countries_result]
        for country in countries:
            country[:] = (attribute for attribute in country if attribute != '')
        return countries

    def get_countries_with_headline(self):
        return [self.get_countries_titles()[1:]] + self.get_countries()

    def log_countries_with_headline_to_csv(self):
        filename = f'{self.html_loader.subject}_{self.html_loader.year}.csv'
        self.logger.info(f'Started writing countries in field {self.html_loader.subject}'
                         f' of year {self.html_loader.year} to {filename}')
        df = pd.DataFrame(self.get_countries_with_headline()[1:], columns=self.get_countries_with_headline()[0])
        df.to_csv(filename, index=False)
        self.logger.info(f'Finished writing countries in field {self.html_loader.subject}'
                         f' of year {self.html_loader.year} to {filename}')
