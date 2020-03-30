"""
    Constants file to be accessed from all of the project
"""
LOGGER_NAME = 'welfare_logger'
LOG_FILE_NAME = 'welfare_log_file.log'
FIRST_YEAR = 2019
SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'
HTTP_SUCCESS = 200
TABLE_HELP_DESC = 'use this option and enter 2 arguments:\
                   \nsubject: {cost-of-living, crime, health-care, pollution, \
                    property-investment, quality-of-life, traffic}\nyear: <year> \
                    many tables can be displayed or copy into csv files. In order \
                     to do so, you will need to enter like the following:' \
                  '<subject1> <year1> <subject2> <year2> <subject3> <year3>...<subjectN> <yearN>'
HELP_DESC = 'Welcome to command line options help. 2 options are available:\
            --table <subject> <year> will return the table wanted. \
            Adding --to_csv will copy the information inquired to a file named <subject>_<year>.csv\
            into the current directory. If no option is entered, all the tables will be downloaded ' \
            'and copy into csv files'
CSV_HELP_DESC = 'this option does not take any argument, if true, this option will copy \
                    the table(s) into a csv(s) file <subject>_<year>.csv into your current directory'