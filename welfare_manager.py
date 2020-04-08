from bs4 import BeautifulSoup
import settings
import argparse
import welfare_html_parser
import DB_manager
import multiprocessing as mp


def log_exception_and_quit(e=None):
    if e is not None:
        settings.logger.critical(e, exc_info=True)
    settings.logger.critical(settings.INVALID_PARAMS)
    settings.exit_program()


def log_ranking(subject, year):
    settings.logger.info(f'Requested ranking of {subject} in {year}')
    html_loader = welfare_html_parser.WelfareHTMLLoader(subject, year)
    html_loader.get_data()
    parser = welfare_html_parser.WelfareHTMLParser(html_loader)
    countries_with_data = parser.get_countries_with_headline()
    settings.countries_data[f'{subject}_{year}'] = countries_with_data
    if not settings.countries_list:
        settings.countries_list = [country_data[0] for country_data in countries_with_data[1:]]
    # We want one line to appear in the log file but a pretty print for the user
    settings.logger.info(settings.countries_data)
    settings.pprint.pprint(settings.countries_data)


def log_all_rankings():
    pool = mp.Pool()
    for subject in settings.WelfareType:
        for year in range(settings.FIRST_YEAR, settings.CURRENT_YEAR):
            # We don't want current_year outputted to the user because the data of the current year isn't full
            pool.apply_async(log_ranking, args=(subject.value, str(year)))
    pool.close()
    pool.join()


def print_tables_of_user_input():
    settings.setup_logger()
    parser = argparse.ArgumentParser(description=settings.HELP_DESC)
    parser.add_argument('--table', nargs='*', action='store', help=settings.TABLE_HELP_DESC)
    parser.add_argument('--all_tables', nargs='*', action='store', help=settings.ALL_TABLES_HELP_DESC)
    try:
        args = parser.parse_args()
    except (ValueError, Exception) as e:
        log_exception_and_quit(e)
    if args.table is None and args.all_tables is None:
        log_exception_and_quit()
    if args.table:
        while args.table:
            try:
                assert args.table[0] in [welfare.value for welfare in settings.WelfareType]
                assert args.table[1] in [str(year) for year in range(settings.FIRST_YEAR, settings.CURRENT_YEAR)]
            except (AssertionError, Exception) as e:
                log_exception_and_quit(e)
            else:
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


def main():
    print_tables_of_user_input()
    store_data_in_DB()


if __name__ == '__main__':
    main()
