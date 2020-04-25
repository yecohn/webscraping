"""
    Global variables to be accessed from all of the project
"""

import logging
import enum
import sys
import collections
import pprint
import requests
import time
import datetime

countries_dict = {}
countries_data = collections.defaultdict(list)
countries_health_data = collections.defaultdict(list)


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

FIRST_YEAR = 2012
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
USERNAME = 'project'
PASSWORD = 'azerty051210'


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


def get_country_id_by_country_code(country_code):
    if country_code not in countries_codes:
        return None
    country_name = countries_codes[country_code]
    if country_name not in countries_dict:
        return None
    return countries_dict[country_name]


countries_codes = {  # ISO Country Code to Country Name
    'AFG': 'Afghanistan',
    'ALA': 'Aland Islands',
    'ALB': 'Albania',
    'DZA': 'Algeria',
    'ASM': 'American Samoa',
    'AND': 'Andorra',
    'AGO': 'Angola',
    'AIA': 'Anguilla',
    'ATA': 'Antarctica',
    'ATG': 'Antigua and Barbuda',
    'ARG': 'Argentina',
    'ARM': 'Armenia',
    'ABW': 'Aruba',
    'AUS': 'Australia',
    'AUT': 'Austria',
    'AZE': 'Azerbaijan',
    'BHS': 'Bahamas',
    'BHR': 'Bahrain',
    'BGD': 'Bangladesh',
    'BRB': 'Barbados',
    'BLR': 'Belarus',
    'BEL': 'Belgium',
    'BLZ': 'Belize',
    'BEN': 'Benin',
    'BMU': 'Bermuda',
    'BTN': 'Bhutan',
    'BOL': 'Bolivia',
    'BIH': 'Bosnia and Herzegovina',
    'BWA': 'Botswana',
    'BVT': 'Bouvet Island',
    'BRA': 'Brazil',
    'VGB': 'British Virgin Islands',
    'IOT': 'British Indian Ocean Territory',
    'BRN': 'Brunei Darussalam',
    'BGR': 'Bulgaria',
    'BFA': 'Burkina Faso',
    'BDI': 'Burundi',
    'KHM': 'Cambodia',
    'CMR': 'Cameroon',
    'CAN': 'Canada',
    'CPV': 'Cape Verde',
    'CYM': 'Cayman Islands',
    'CAF': 'Central African Republic',
    'TCD': 'Chad',
    'CHL': 'Chile',
    'CHN': 'China',
    'HKG': 'Hong Kong, Special Administrative Region of China',
    'MAC': 'Macao, Special Administrative Region of China',
    'CXR': 'Christmas Island',
    'CCK': 'Cocos (Keeling) Islands',
    'COL': 'Colombia',
    'COM': 'Comoros',
    'COG': 'Congo (Brazzaville)',
    'COD': 'Congo, Democratic Republic of the',
    'COK': 'Cook Islands',
    'CRI': 'Costa Rica',
    'CIV': 'Cote d\'Ivoire',
    'HRV': 'Croatia',
    'CUB': 'Cuba',
    'CYP': 'Cyprus',
    'CZE': 'Czech Republic',
    'DNK': 'Denmark',
    'DJI': 'Djibouti',
    'DMA': 'Dominica',
    'DOM': 'Dominican Republic',
    'ECU': 'Ecuador',
    'EGY': 'Egypt',
    'SLV': 'El Salvador',
    'GNQ': 'Equatorial Guinea',
    'ERI': 'Eritrea',
    'EST': 'Estonia',
    'ETH': 'Ethiopia',
    'FLK': 'Falkland Islands (Malvinas)',
    'FRO': 'Faroe Islands',
    'FJI': 'Fiji',
    'FIN': 'Finland',
    'FRA': 'France',
    'GUF': 'French Guiana',
    'PYF': 'French Polynesia',
    'ATF': 'French Southern Territories',
    'GAB': 'Gabon',
    'GMB': 'Gambia',
    'GEO': 'Georgia',
    'DEU': 'Germany',
    'GHA': 'Ghana',
    'GIB': 'Gibraltar',
    'GRC': 'Greece',
    'GRL': 'Greenland',
    'GRD': 'Grenada',
    'GLP': 'Guadeloupe',
    'GUM': 'Guam',
    'GTM': 'Guatemala',
    'GGY': 'Guernsey',
    'GIN': 'Guinea',
    'GNB': 'Guinea-Bissau',
    'GUY': 'Guyana',
    'HTI': 'Haiti',
    'HMD': 'Heard Island and Mcdonald Islands',
    'VAT': 'Holy See (Vatican City State)',
    'HND': 'Honduras',
    'HUN': 'Hungary',
    'ISL': 'Iceland',
    'IND': 'India',
    'IDN': 'Indonesia',
    'IRN': 'Iran, Islamic Republic of',
    'IRQ': 'Iraq',
    'IRL': 'Ireland',
    'IMN': 'Isle of Man',
    'ISR': 'Israel',
    'ITA': 'Italy',
    'JAM': 'Jamaica',
    'JPN': 'Japan',
    'JEY': 'Jersey',
    'JOR': 'Jordan',
    'KAZ': 'Kazakhstan',
    'KEN': 'Kenya',
    'KIR': 'Kiribati',
    'PRK': 'Korea, Democratic People\'s Republic of',
    'KOR': 'Korea, Republic of',
    'KWT': 'Kuwait',
    'KGZ': 'Kyrgyzstan',
    'LAO': 'Lao PDR',
    'LVA': 'Latvia',
    'LBN': 'Lebanon',
    'LSO': 'Lesotho',
    'LBR': 'Liberia',
    'LBY': 'Libya',
    'LIE': 'Liechtenstein',
    'LTU': 'Lithuania',
    'LUX': 'Luxembourg',
    'MKD': 'Macedonia, Republic of',
    'MDG': 'Madagascar',
    'MWI': 'Malawi',
    'MYS': 'Malaysia',
    'MDV': 'Maldives',
    'MLI': 'Mali',
    'MLT': 'Malta',
    'MHL': 'Marshall Islands',
    'MTQ': 'Martinique',
    'MRT': 'Mauritania',
    'MUS': 'Mauritius',
    'MYT': 'Mayotte',
    'MEX': 'Mexico',
    'FSM': 'Micronesia, Federated States of',
    'MDA': 'Moldova',
    'MCO': 'Monaco',
    'MNG': 'Mongolia',
    'MNE': 'Montenegro',
    'MSR': 'Montserrat',
    'MAR': 'Morocco',
    'MOZ': 'Mozambique',
    'MMR': 'Myanmar',
    'NAM': 'Namibia',
    'NRU': 'Nauru',
    'NPL': 'Nepal',
    'NLD': 'Netherlands',
    'ANT': 'Netherlands Antilles',
    'NCL': 'New Caledonia',
    'NZL': 'New Zealand',
    'NIC': 'Nicaragua',
    'NER': 'Niger',
    'NGA': 'Nigeria',
    'NIU': 'Niue',
    'NFK': 'Norfolk Island',
    'MNP': 'Northern Mariana Islands',
    'NOR': 'Norway',
    'OMN': 'Oman',
    'PAK': 'Pakistan',
    'PLW': 'Palau',
    'PSE': 'Palestinian Territory, Occupied',
    'PAN': 'Panama',
    'PNG': 'Papua New Guinea',
    'PRY': 'Paraguay',
    'PER': 'Peru',
    'PHL': 'Philippines',
    'PCN': 'Pitcairn',
    'POL': 'Poland',
    'PRT': 'Portugal',
    'PRI': 'Puerto Rico',
    'QAT': 'Qatar',
    'REU': 'Reunion',
    'ROU': 'Romania',
    'RUS': 'Russian Federation',
    'RWA': 'Rwanda',
    'BLM': 'Saint-Barthelemy',
    'SHN': 'Saint Helena',
    'KNA': 'Saint Kitts and Nevis',
    'LCA': 'Saint Lucia',
    'MAF': 'Saint-Martin (French part)',
    'SPM': 'Saint Pierre and Miquelon',
    'VCT': 'Saint Vincent and Grenadines',
    'WSM': 'Samoa',
    'SMR': 'San Marino',
    'STP': 'Sao Tome and Principe',
    'SAU': 'Saudi Arabia',
    'SEN': 'Senegal',
    'SRB': 'Serbia',
    'SYC': 'Seychelles',
    'SLE': 'Sierra Leone',
    'SGP': 'Singapore',
    'SVK': 'Slovakia',
    'SVN': 'Slovenia',
    'SLB': 'Solomon Islands',
    'SOM': 'Somalia',
    'ZAF': 'South Africa',
    'SGS': 'South Georgia and the South Sandwich Islands',
    'SSD': 'South Sudan',
    'ESP': 'Spain',
    'LKA': 'Sri Lanka',
    'SDN': 'Sudan',
    'SUR': 'Suriname',
    'SJM': 'Svalbard and Jan Mayen Islands',
    'SWZ': 'Swaziland',
    'SWE': 'Sweden',
    'CHE': 'Switzerland',
    'SYR': 'Syrian Arab Republic (Syria)',
    'TWN': 'Taiwan, Republic of China',
    'TJK': 'Tajikistan',
    'TZA': 'Tanzania, United Republic of',
    'THA': 'Thailand',
    'TLS': 'Timor-Leste',
    'TGO': 'Togo',
    'TKL': 'Tokelau',
    'TON': 'Tonga',
    'TTO': 'Trinidad and Tobago',
    'TUN': 'Tunisia',
    'TUR': 'Turkey',
    'TKM': 'Turkmenistan',
    'TCA': 'Turks and Caicos Islands',
    'TUV': 'Tuvalu',
    'UGA': 'Uganda',
    'UKR': 'Ukraine',
    'ARE': 'United Arab Emirates',
    'GBR': 'United Kingdom',
    'USA': 'United States of America',
    'UMI': 'United States Minor Outlying Islands',
    'URY': 'Uruguay',
    'UZB': 'Uzbekistan',
    'VUT': 'Vanuatu',
    'VEN': 'Venezuela (Bolivarian Republic of)',
    'VNM': 'Viet Nam',
    'VIR': 'Virgin Islands, US',
    'WLF': 'Wallis and Futuna Islands',
    'ESH': 'Western Sahara',
    'YEM': 'Yemen',
    'ZMB': 'Zambia',
    'ZWE': 'Zimbabwe'
}
