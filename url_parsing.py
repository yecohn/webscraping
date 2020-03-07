from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import pandas as pd
import csv


class HtmlContent:

    def __init__(self, url):
        self.url = url

    def g_url(self):
        return requests.get(self.url)

    def parse_response(self):
        return BeautifulSoup(self.g_url().text, 'html.parser')

    def html_print(self):

        data = self.parse_response()
        print(data)


class get_info(HtmlContent):
    def name_marker(self):
         a = []
         tag = self.parse_response().find_all('th')
         for word in tag:
             a.append(word.get_text())

         return a

    def country_data_html(self):
        info = []
        for article in self.parse_response().find_all('tr', style='width: 100%'):
            headline = article.text
            info.append(headline)
        info_2 = [a.split('\n') for a in info]

        for a in info_2:
            a[:] = (i for i in a if i != '')
        return info_2

    def scrapping_file(self):
        return [self.name_marker()[1:]] + self.country_data_html()



       # tags = tags.text
       # tag2 = tags.find_all()
        #for tag in tags:
        #    info = []
        #    tmp = tag.split('\n')
        #    tmp[:] = (val for val in info if val != '')
        #    info.append(tmp)
        return info



    def country_data(self):
        pass
def main():

    URL = 'https://www.numbeo.com/cost-of-living/rankings_by_country.jsp'
    cost = get_info(URL)
    #print(cost.name_marker())
    print(cost.scrapping_file())
    frame = pd.DataFrame(cost.scrapping_file()[1:], columns = cost.scrapping_file()[0])
    print(frame.head(10)[0:3])
    frame.to_csv('cost_of_living_2020.csv', index=False)




if __name__ == '__main__':
    main()
