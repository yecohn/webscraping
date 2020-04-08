from bs4 import BeautifulSoup
import config
import argparse
import welfare_html_parser
import DB_manager
import multiprocessing as mp


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
    config.countries_data[f'{subject}_{year}'] = countries_with_data
    for index, country_data in enumerate(countries_with_data[1:]):
        config.countries_dict[country_data[0]] = index + 1
    # We want one line to appear in the log file but a pretty print for the user
    config.logger.info(config.countries_data)
    config.pprint.pprint(config.countries_data)


def log_all_rankings(asynchronous=True):
    if asynchronous:
        pool = mp.Pool()
    for subject in config.WelfareType:
        for year in range(config.FIRST_YEAR, config.CURRENT_YEAR):
            # We don't want current_year outputted to the user because the data of the current year isn't full
            if asynchronous:
                pool.apply_async(log_ranking, args=(subject.value, str(year)))
            else:
                log_ranking(subject.value, str(year))
    if asynchronous:
        pool.close()
        pool.join()


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
                assert args.table[1] in [str(year) for year in range(config.FIRST_YEAR, config.CURRENT_YEAR)]
            except (AssertionError, Exception) as e:
                log_exception_and_quit(e)
            else:
                print('\n\n\n')
                log_ranking(args.table[0], args.table[1])
                print('\n\n\n')
                del args.table[:2]
    else:  # all tables
        log_all_rankings(asynchronous=False)


def store_data_in_DB():
    db_manager = DB_manager.DBManager()
    db_manager.connect_to_DB()
    db_manager.setup_DB()
    db_manager.close_DB()


def main():
    config.setup()
    print_tables_of_user_input()
    store_data_in_DB()


if __name__ == '__main__':
    main()
