import config
import argparse
import welfare_html_parser
import DB_manager
from health_api_data_manager import HealthAPIDataManager

countries = []


def log_exception_and_quit(e=None):
    if e is not None:
        config.logger.critical(e, exc_info=True)
    config.logger.critical(config.INVALID_PARAMS)
    config.exit_program()


def log_ranking(subject, year):
    config.logger.info(f'Requested ranking of {subject} in {year}')
    html_loader = welfare_html_parser.WelfareHTMLLoader(subject, year)
    html_loader.get_data()
    parser = welfare_html_parser.WelfareHTMLParser(html_loader)
    countries_with_data = parser.get_countries_with_headline()
    if len(countries_with_data) > 1:
        countries.extend(list(zip(*countries_with_data[1:]))[0])
    subject_corrected = subject.replace('-', '_')
    config.countries_data[f'{subject_corrected}_{year}'] = countries_with_data
    # We want one line to appear in the log file but a pretty print for the user
    config.logger.info(config.countries_data)
    config.pprint.pprint(config.countries_data)


def log_all_rankings():
    for subject in config.WelfareType:
        for year in range(config.FIRST_YEAR, config.LAST_YEAR + 1):
            log_ranking(subject.value, str(year))
    for index, country_data in enumerate(set(countries)):
        config.countries_dict[country_data] = index + 1


def print_tables_of_user_input():
    parser = argparse.ArgumentParser(description=config.HELP_DESC)
    parser.add_argument('--table', nargs='*', action='store', help=config.TABLE_HELP_DESC)
    parser.add_argument('--all_tables', nargs='*', action='store', help=config.ALL_TABLES_HELP_DESC)
    try:
        args = parser.parse_args()
    except (ValueError, Exception) as e:
        log_exception_and_quit(e)
    if args.table is None and args.all_tables is None:
        log_exception_and_quit()
    if args.table:
        while args.table:
            try:
                assert args.table[0] in [welfare.value for welfare in config.WelfareType]
                assert args.table[1] in [str(year) for year in range(config.FIRST_YEAR, config.LAST_YEAR + 1)]
            except (AssertionError, Exception) as e:
                log_exception_and_quit(e)
                print('\n\n\n')
                log_ranking(args.table[0], args.table[1])
                print('\n\n\n')
                del args.table[:2]
    else:  # all tables
        log_all_rankings()


def store_data_in_DB():
    db_manager = DB_manager.DBManager()
    db_manager.connect_to_DB()
    db_manager.setup_DB()
    db_manager.close_DB()


def main():
    start_time = config.time.time()
    config.setup()
    print_tables_of_user_input()
    HealthAPIDataManager.get_data()
    store_data_in_DB()
    end_time = config.time.time()
    print(f'Seconds taken: {end_time - start_time}')


if __name__ == '__main__':
    main()
