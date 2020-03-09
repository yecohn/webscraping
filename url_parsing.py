from bs4 import BeautifulSoup
import requests
import pandas as pd


class HTMLLoader:

    def __init__(self, url):
        self.url = url

    def get_data_from_url(self):
        return requests.get(self.url).text

    def parse_response(self):
        return BeautifulSoup(self.get_data_from_url(), 'html.parser')

    def print_HTML(self):
        print(self.parse_response())


class Adapter:

    def __init__(self, html_loader):
        self.html_data = html_loader.parse_response()

    def get_countries_titles(self):
        tags = self.html_data.find_all('th')
        return [tag.get_text() for tag in tags]

    def get_countries(self):
        countries_result = []
        countries_html = self.html_data.find_all('tr', style="width: 100%")
        [countries_result.append(country.text) for country in countries_html]
        countries = [item.split('\n') for item in countries_result]
        for country in countries:
            country[:] = (attribute for attribute in country if attribute != '')
        return countries

    def get_countries_with_headline(self):
        return [self.get_countries_titles()[1:]] + self.get_countries()

    def print_countries_with_headline_to_csv(self):
        dataframe = pd.DataFrame(self.get_countries_with_headline()[1:], columns=self.get_countries_with_headline()[0])
        dataframe.to_csv('cost_of_living_2020.csv', index=False)


def main():
    URL = 'https://www.numbeo.com/health-care/rankings_by_country.jsp?title=2019'
    html_loader = HTMLLoader(URL)
    adapter = Adapter(html_loader)
    adapter.print_countries_with_headline_to_csv()


if __name__ == '__main__':
    main()
