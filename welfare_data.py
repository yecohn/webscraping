from bs4 import BeautifulSoup
import requests
import re
from enum import Enum
from welfare_html_parser import HTMLLoader
from welfare_html_parser import HTMLAdapter
import datetime
import argparse
import sys

SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
FIRST_YEAR = 2010
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'


class Welfare(Enum):
    cost_of_living = 'cost-of-living'
    crime = 'crime'
    health_care = 'health-care'
    pollution = 'pollution'
    property_investment = 'property-investment'
    quality_of_life = 'quality-of-life'
    traffic = 'traffic'


def log_ranking(subject, year):
    URL = MAIN_URL.replace(SUBJECT, subject).replace(YEAR, year)
    html_loader = HTMLLoader(URL, subject, year)
    adapter = HTMLAdapter(html_loader)
    return adapter.get_countries_with_headline()


def log_ranking_to_csv(subject, year):
    URL = MAIN_URL.replace(SUBJECT, subject).replace(YEAR, year)
    html_loader = HTMLLoader(URL, subject, year)
    adapter = HTMLAdapter(html_loader)
    adapter.log_countries_with_headline_to_csv()

def log_all_year(subject):
    current_year = int(datetime.datetime.now().year)
    for year in range(FIRST_YEAR, current_year + 1):  # We don't want this current year in the csv because it's not full
            log_ranking(subject, str(year))


def log_all_rankings_to_csvs():
    current_year = int(datetime.datetime.now().year)
    for welfare in Welfare:
        for year in range(FIRST_YEAR, current_year + 1):  # We don't want this current year in the csv because it's not full
            log_ranking_to_csv(welfare.value, str(year))




def main():

    parser = argparse.ArgumentParser(description= 'Welcolme to command line options help. 2 options are available:\
                                                    --table <subject> <year> will return the table wanted. \
                                                    Adding --to_csv will copy the information inquired to a file named <subject><year>.csv\
                                                    into the current directory. \
                                                    If no option is entered, all the tables will be downloaded and copy into csv files')

    parser.add_argument('--table', nargs = '*' , action= 'store', help = 'use this option and enter 2 arguments:\
                                                                         subject: {cost-of-living, crime, health-care, pollution, \
                                                                         property-investment, quality-of-life, traffic} year: <year> \
                                                                         many tables can be displayed or copy into csv files. In order \
                                                                         to do so, you will need to enter <subject1> <year1> <subject2> \
                                                                           ... <subjectn> <yearn>')


    parser.add_argument('--to_csv',   action = 'store_true', help= 'this option does not take any argument, if true, this option will copy \
                                                                    the table(s) into a csv(s) file <subject>_<year>.csv into your current directory' )
    args = parser.parse_args()

    if args.table:
        counter = 0
        while len(args.table) != 0:
            try:
                try:
                    assert args.table[0] in [welfare.value for welfare in Welfare]

                    assert args.table[1] in [str(i) for i in range(2009, 2020)]
                except (AssertionError, Exception) as err:


                    print('you enter a wrong parameter for your {}th iteration. parameter {} or {} is not valid.  use --help for more information '.format(counter + 1, args.table[0], args.table[1]))
                    sys.exit()
                else:
                    if args.to_csv:

                                log_ranking_to_csv(*args.table[0:2])
                                print('file {}_{}.csv has been created in your current directory'.format(args.table[0], args.table[1]))
                                counter += 1
                                args.table.pop(0)
                                args.table.pop(0)
                    else:



                               print('List number: {} is displayed '.format(counter + 1))
                               print(' \n \n \n ')
                               [print(i) for i in log_ranking(*args.table[0:2])]
                               print(' \n \n \n ')
                               args.table.pop(0)
                               args.table.pop(0)
                               counter += 1
            except (TypeError, Exception) as err:
                print(err)
                sys.exit()
    else:
        log_all_rankings_to_csvs()


if __name__ == '__main__':
    main()


