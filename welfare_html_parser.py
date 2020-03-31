from bs4 import BeautifulSoup
import requests
import pandas as pd
<<<<<<< HEAD
import argparse
HTTP_SUCCESS = 200
=======
import logging
import settings
import sys
>>>>>>> 38992ae2c09ba57a5c65fd0665d68be7da1b93a5


class HTMLLoader:

<<<<<<< HEAD
    def __init__(self, url, subject, year):
        self.url = url
=======
    def __init__(self, subject, year):
        self.url = settings.MAIN_URL.replace(settings.SUBJECT, subject).replace(settings.YEAR, year)
>>>>>>> 38992ae2c09ba57a5c65fd0665d68be7da1b93a5
        self.subject = subject
        self.year = year

<<<<<<< HEAD
    def get_data_from_url(self):
        response = requests.get(self.url)
        if response.status_code == HTTP_SUCCESS and type(response.text) == str:
            return response.text
        print('Failed to download data from server!')
        exit()
=======
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
            sys.exit()
        self.logger.info(f'Finished fetching data from {self.url}')
        if response.status_code != settings.HTTP_SUCCESS:
            self.logger.critical(e, exc_info=True)
            sys.exit()
        return response.text
>>>>>>> 38992ae2c09ba57a5c65fd0665d68be7da1b93a5

    def parse_response(self):
        try:
<<<<<<< HEAD
            soup = BeautifulSoup(self.get_data_from_url(), 'html.parser')
        except:
            print("Failed to parse the data!")
            exit()
        return soup

    def print_HTML(self):
        print(self.parse_response())
=======
            self.response_soup = BeautifulSoup(self.response_text, 'html.parser')
            self.logger.info(f'Finished parsing response from {self.url}')
            return self.response_soup
        except (TypeError, Exception) as e:
            self.logger.critical(e, exc_info=True)
            sys.exit()
>>>>>>> 38992ae2c09ba57a5c65fd0665d68be7da1b93a5


class HTMLAdapter:

    def __init__(self, html_loader):
        self.html_loader = html_loader

    def get_countries_titles(self):
        tags = self.html_loader.parse_response().find_all('th')
        return [tag.get_text() for tag in tags]

    def get_countries(self):
        countries_result = []
        countries_html = self.html_loader.parse_response().find_all('tr', style="width: 100%")
        [countries_result.append(country.text) for country in countries_html]
        countries = [item.split('\n') for item in countries_result]
        for country in countries:
            country[:] = (attribute for attribute in country if attribute != '')
        return countries

    def get_countries_with_headline(self):
        return [self.get_countries_titles()[1:]] + self.get_countries()

    def log_countries_with_headline_to_csv(self):
        dataframe = pd.DataFrame(self.get_countries_with_headline()[1:], columns=self.get_countries_with_headline()[0])
        dataframe.to_csv(f'{self.html_loader.subject}_{self.html_loader.year}.csv', index=False)








