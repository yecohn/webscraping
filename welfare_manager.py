from bs4 import BeautifulSoup
from enum import Enum
from welfare_html_parser import HTMLLoader
from welfare_html_parser import HTMLAdapter
import datetime
import logging
import settings
import sys
import argparse


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
        self.setup_logger()

    def setup_logger(self):
        file_handler = logging.FileHandler(settings.LOG_FILE_NAME)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)  # write to the file LOG_FILE_NAME
        self.logger.addHandler(logging.StreamHandler(sys.stdout))  # adds print to console
        self.logger.level = logging.INFO

    def log_all_subjects_rankings_to_csvs(self, year):
        current_year = int(datetime.datetime.now().year)
        for welfare_type in WelfareType:
            # We don't want current_year outputted to the user because that data of the current year isn't full
            self.log_ranking_to_csv(welfare_type.value, str(year))

    def log_ranking(self, subject, year):
        html_loader = HTMLLoader(subject, year)
        html_loader.get_data()
        adapter = HTMLAdapter(html_loader)
        return adapter.get_countries_with_headline()

    def log_all_years_ranking(self, subject):
        current_year = int(datetime.datetime.now().year)
        for year in range(settings.FIRST_YEAR, current_year):
            # We don't want current_year outputted to the user because the data of the current year isn't full
            self.log_ranking(subject, str(year))

    def log_ranking_to_csv(self, subject, year):
        html_loader = HTMLLoader(subject, year)
        html_loader.get_data()
        adapter = HTMLAdapter(html_loader)
        adapter.log_countries_with_headline_to_csv()

    def log_all_subjects_and_years_rankings_to_csvs(self):
        current_year = int(datetime.datetime.now().year)
        for welfare_type in WelfareType:
            for year in range(settings.FIRST_YEAR, current_year):
                # We don't want current_year outputted to the user because the data of the current year isn't full
                self.log_ranking_to_csv(welfare_type.value, str(year))


""" Comment for Yaniv: here the command line interface. 
I added it into the main. We should discuss how we want to display it 
but for now. the main is designed to be run from the command line. 
It the user is doing python welfare_manager.py --help the help 
doc will appear. there he will learn how to use the different options.
In order to build the database on your computer you should go to db_building.py 
and change your connection setting: in the mydb = ...
for the sake of the exercise I did not hide my information. We should howerver
"""


def main():

    welfare_manager = WelfareManager()
    parser = argparse.ArgumentParser(description=settings.HELP_DESC)
    parser.add_argument('--table', nargs='*', action='store', help=settings.TABLE_HELP_DESC)
    parser.add_argument('--csv', action='store_true', help=settings.CSV_HELP_DESC)
    args = parser.parse_args()
    current_year = int(datetime.datetime.now().year)
    if args.table:
        counter = 0
        while len(args.table) != 0:
            try:
                try:
                    assert args.table[0] in [welfare.value for welfare in WelfareType]
                    assert args.table[1] in [str(i) for i in range(settings.FIRST_YEAR, current_year)]
                except (AssertionError, Exception) as err:

                    print(f'You have entered a wrong parameter for your {counter + 1}th iteration.\n'
                          f'Parameters {args.table[0]} and {args.table[1]} are not valid.\n'
                          f'Use --help for more information')
                    sys.exit()
                else:
                    if args.to_csv:
                        welfare_manager.log_ranking_to_csv(*args.table[0:2])
                        print(f'File {args.table[0]}_{args.table[1]}.csv has been created in your current directory')
                        counter += 1
                        args.table.clear()
                    else:
                        print(f'List number: {counter + 1} is displayed ')
                        print(' \n \n \n ')
                        [print(i) for i in welfare_manager.log_ranking(args.table[0], args.table[1])]
                        print(' \n \n \n ')
                        args.table.pop(0)
                        args.table.pop(0)
                        counter += 1
            except (TypeError, Exception) as err:
                print(err)
                sys.exit()
    else:
        welfare_manager.log_all_subjects_and_years_rankings_to_csvs()


if __name__ == '__main__':
    main()
