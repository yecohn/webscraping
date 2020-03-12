from bs4 import BeautifulSoup
import requests
import pandas as pd

HTTP_SUCCESS = 200


class HTMLLoader:

    def __init__(self, url, subject, year):
        self.url = url
        self.subject = subject
        self.year = year

    def get_data_from_url(self):
        response = requests.get(self.url)
        if response.status_code == HTTP_SUCCESS and type(response.text) == str:
            return response.text
        print('Failed to download data from server!')
        exit()

    def parse_response(self):
        try:
            soup = BeautifulSoup(self.get_data_from_url(), 'html.parser')
        except:
            print("Failed to parse the data!")
            exit()

    def print_HTML(self):
        print(self.parse_response())


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
