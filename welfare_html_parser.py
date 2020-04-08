from bs4 import BeautifulSoup
import requests
import config


class WelfareHTMLLoader:

    def __init__(self, subject, year):
        self.url = config.MAIN_URL.replace(config.SUBJECT, subject).replace(config.YEAR, year)
        self.subject = subject
        self.year = year
        self.response_text = None
        self.response_soup = None

    def get_data(self):
        self.response_text = self._fetch_text_from_url()
        self.response_soup = self._parse_response()
        return self.response_soup

    def _fetch_text_from_url(self):
        config.logger.info(f'Started fetching data from {self.url}')
        try:
            response = requests.get(self.url)
        except (TypeError, ConnectionError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()
        if response.status_code != config.HTTP_SUCCESS:
            config.logger.critical(f'Error fetching data from {self.url}')
            config.exit_program()
        config.logger.info(f'Finished fetching data from {self.url}')
        return response.text

    def _parse_response(self):
        config.logger.info(f'Started parsing response from {self.url}')
        try:
            self.response_soup = BeautifulSoup(self.response_text, 'html.parser')
            config.logger.info(f'Finished parsing response from {self.url}')
            return self.response_soup
        except (TypeError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()


class WelfareHTMLParser:

    def __init__(self, html_loader):
        self.html_loader = html_loader

    def _get_countries_subject_indexes(self):
        tags = self.html_loader.response_soup.find_all('th')
        return [tag.get_text() for tag in tags]

    def _get_countries_data(self):
        countries_result = []
        countries_html = self.html_loader.response_soup.find_all('tr', style="width: 100%")
        [countries_result.append(country.text) for country in countries_html]
        countries = [item.split('\n') for item in countries_result]
        for country in countries:
            country[:] = (attribute for attribute in country if attribute != '')
        return countries

    def get_countries_with_headline(self):
        return [self._get_countries_subject_indexes()[1:]] + self._get_countries_data()
