"""
    Global variables to be accessed from all of the project
"""

import logging
import enum
import sys
import collections
import requests
import time
import datetime
import pprint

countries_dict = {}
countries_data = collections.defaultdict(list)
countries_health_data = collections.defaultdict(list)
countries_codes = {}


class HealthIndicator(enum.Enum):
    road_death_rate = 'RS_198'
    pollution_death_rate = 'SDGAIRBOD'


class WelfareType(enum.Enum):
    cost_of_living = 'cost-of-living'
    crime = 'crime'
    health_care = 'health-care'
    quality_of_life = 'quality-of-life'
    property_investment = 'property-investment'
    traffic = 'traffic'
    pollution = 'pollution'


LOGGER_NAME = 'welfare_logger'
logger = logging.getLogger(LOGGER_NAME)

FIRST_YEAR = 2019
LAST_YEAR = 2019

# Logger
LOG_FILE_NAME = 'welfare_log_file.log'

# URL Requests/Responses
SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
HEALTH_INDICATOR = '<INDICATOR>'
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'
HEALTH_INDICATORS_URL = 'https://ghoapi.azureedge.net/api/Indicator'
HEALTH_INDICATOR_URL = f'https://ghoapi.azureedge.net/api/{HEALTH_INDICATOR}'
HTTP_SUCCESS = 200

# Command Line Interface
welfare_types_string = ', '.join([welfare_type.value for welfare_type in WelfareType])
TABLE_HELP_DESC = f'''Run this command to receive only one table with the following 2 arguments:
                   \nsubject: {welfare_types_string}
                    \nyear: ranges from {FIRST_YEAR} to {LAST_YEAR} 
                    Please run the command in the following manner:
                    <subject1> <year1> <subject2> <year2> <subject3> <year3>...<subjectN> <yearN>'''
ALL_TABLES_HELP_DESC = '''Run this command to receive all of the tables'''
HELP_DESC = 'You have 2 available commands: --table and --all_tables'
INVALID_PARAMS = 'You have entered invalid parameters\n' + HELP_DESC

# MySQL
DATABASE_NAME = 'welfare'
HOST = 'localhost'
USERNAME = 'root'
PASSWORD = 'Yc7350328'


def exit_program():
    sys.exit()


def setup():
    setup_logger()


def setup_logger():
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    formatter = logging.Formatter(
        '[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        '%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)  # write to the file LOG_FILE_NAME
    logger.addHandler(logging.StreamHandler(sys.stdout))  # adds print to console
    logger.level = logging.INFO
