import mysql.connector
import settings


class DBManager:

    def __init__(self):
        try:
            self.welfare_db = mysql.connector.connect(host=settings.HOST,
                                                      user=settings.USERNAME,
                                                      passwd=settings.PASSWORD)
        except (TypeError, ValueError, ConnectionError, Exception) as e:
            settings.logger.critical(e, exc_info=True)
            settings.exit_program()
        self.cur = self.welfare_db.cursor()

    def connect_to_DB(self):
        self.cur.execute(f'DROP DATABASE IF EXISTS {settings.DATABASE_NAME}')
        self.cur.execute(f'CREATE DATABASE {settings.DATABASE_NAME}')
        self.cur.execute(f'USE {settings.DATABASE_NAME}')
        settings.logger.info(f'Connected to DB "{settings.DATABASE_NAME}"')

    def setup_DB(self):
        self._create_table_countries()
        self._create_table_property_price()
        self._close_DB()
        settings.logger.info(f'Finished setting up DB "{settings.DATABASE_NAME}"')

    def _close_DB(self):
        self.welfare_db.close()

    def _create_table_countries(self):
        self.cur.execute('''CREATE TABLE countries( country_id INT AUTO_INCREMENT PRIMARY KEY,
                                                    country_name VARCHAR(255))''')
        self.welfare_db.commit()
        query = "INSERT INTO countries (country_name) VALUES (%s)"
        countries_list_tuples = [(country, ) for country in settings.countries_list]
        self.cur.executemany(query, countries_list_tuples)
        self.welfare_db.commit()
        settings.logger.info('Created table "countries"')

    def _create_table_property_price(self):
        self.cur.execute('''CREATE TABLE  property_price(
                                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                                        country_id INT,
                                                        year INT,
                                                        price_to_income FLOAT,
                                                        gross_rental_inside_center FLOAT,
                                                        gross_rental_outside_center FLOAT,
                                                        price_rent_city_center FLOAT,
                                                        price_rent_outside_city_center FLOAT,
                                                        mortgage_as_prc_income FLOAT,
                                                        affordability FLOAT,
                                                        FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                        )''')
        self.welfare_db.commit()

        subject = settings.WelfareType.property_investment.value
        years = list(map(str, range(2010, settings.CURRENT_YEAR)))
        for year in years:
            for row in settings.countries_data[f'{subject}_{year}'][1:]:
                self.cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
                self.cur.execute("INSERT INTO property_price (country_id, year, price_to_income, gross_rental_inside_center, gross_rental_outside_center, \
                                   price_rent_city_center, \
                                   price_rent_outside_city_center, mortgage_as_prc_income, affordability) VALUES \
                                   (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 'fields')



        # cur.execute('''CREATE TABLE  cost_of_living(
        #                                id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                country_id INT,
        #                                year INT,
        #                                cost_of_living FLOAT,
        #                                rent FLOAT,
        #                                cost_of_living_and_rent FLOAT,
        #                                groceries_prices FLOAT,
        #                                restaurant_prices FLOAT,
        #                                local_purchasing_power FLOAT,
        #                                FOREIGN KEY (country_id) REFERENCES countries(country_id)
        #                                )''')
        # SUBJECT_NAME = 'cost-of-living'
        # YEARS = [str(year) for year in range(2010, settings.CURRENT_YEAR + 1)]
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #         cur.execute("INSERT INTO cost_of_living (country_id, year, cost_of_living, rent, cost_of_living_and_rent, \
        #                                    groceries_prices, restaurant_prices, local_purchasing_power) VALUES \
        #                                    (%s, %s, %s, %s, %s, %s, %s, %s)", fields)
        # mydb.commit()
        #
        # cur.execute('''CREATE TABLE  traffic(
        #                                id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                country_id INT,
        #                                year INT,
        #                                traffic_id FLOAT,
        #                                time_id FLOAT,
        #                                time_exp_id FLOAT,
        #                                inefficiency_id FLOAT,
        #                                CO2_emission_id FLOAT,
        #                                foreign key (country_id) references countries(country_id)
        #                                )''')
        # SUBJECT_NAME = 'traffic'
        # YEARS = [str(year) for year in range(2010, settings.CURRENT_YEAR + 1)]
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #         cur.execute("INSERT INTO traffic (country_id, year, traffic_id, time_id, time_exp_id, inefficiency_id , \
        #                                    CO2_emission_id) VALUES \
        #                                    (%s, %s, %s, %s, %s, %s, %s)", fields)
        #
        # mydb.commit()
        #
        # cur.execute('''CREATE TABLE  health_care(
        #                                 id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                 country_id INT,
        #                                 year INT,
        #                                 health_care_id FLOAT,
        #                                 health_care_exp_id FLOAT,
        #                                 foreign key (country_id) references countries(country_id)
        #                                 )''')
        # SUBJECT_NAME = 'health-care'
        # YEARS = [str(year) for year in range(2010, settings.CURRENT_YEAR + 1)]
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #         cur.execute("INSERT INTO health_care (country_id, year,health_care_id, health_care_exp_id) VALUES \
        #                                     (%s,%s, %s, %s)", fields)
        #
        # mydb.commit()
        #
        # cur.execute('''CREATE TABLE  pollution(
        #                                 id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                 country_id INT,
        #                                 year INT,
        #                                 pollution_id INT,
        #                                 exp_pollution_id INT,
        #                                 foreign key (country_id) references countries(country_id)
        #                                 )''')
        # SUBJECT_NAME = 'pollution'
        # YEARS = [str(year) for year in range(2010, settings.CURRENT_YEAR + 1)]
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #         cur.execute("INSERT INTO pollution (country_id, year, pollution_id, exp_pollution_id) VALUES \
        #                                     (%s ,%s, %s, %s)", fields)
        #
        # mydb.commit()
        #
        # cur.execute('''CREATE TABLE  quality_life(
        #                                 id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                 country_id INT,
        #                                 year INT,
        #                                 quality_life_id FLOAT,
        #                                 purchase_power_id FLOAT,
        #                                 safety_id FLOAT,
        #                                 health_care_id FLOAT,
        #                                 cost_living_id FLOAT,
        #                                 property_price_to_income_id FLOAT,
        #                                 traffic_commute_time_id FLOAT,
        #                                 pollution_id FLOAT,
        #                                 climate_id VARCHAR(255),
        #                                 foreign key (country_id) references countries(country_id)
        #                                 )''')
        # SUBJECT_NAME = 'quality-of-life'
        # YEARS = [str(year) for year in range(2010, settings.CURRENT_YEAR + 1)]
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #
        #         cur.execute("INSERT INTO quality_life (country_id, year, quality_life_id, purchase_power_id, safety_id, \
        #                                     health_care_id, cost_living_id, property_price_to_income_id, \
        #                                     traffic_commute_time_id, pollution_id, climate_id) VALUES \
        #                                      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", fields)
        #
        # mydb.commit()
        #
        # cur.execute('''CREATE TABLE  crime(
        #                                 id  INT PRIMARY KEY AUTO_INCREMENT,
        #                                 country_id INT,
        #                                 year INT,
        #                                 crime_id FLOAT,
        #                                 safety_id FLOAT,
        #                                 foreign key (country_id) references countries(country_id)
        #                                 )''')
        # SUBJECT_NAME = 'crime'
        # YEARS = [str(year) for year in range(2010, Settingssettings.CURRENT_YEAR + 1)]
        #
        # for year in YEARS:
        #     for row in welfare_manager.log_ranking(SUBJECT_NAME, year)[1:]:
        #         if row[0] in dic_country:
        #             print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #         else:
        #             dic_country[row[0]] = counter
        #             counter += 1
        #             fields = [dic_country[row[0]], year, *row[1:]]
        #             cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
        #             mydb.commit()
        #         cur.execute("INSERT INTO crime (country_id, year, crime_id, safety_id) VALUES \
        #                                     (%s, %s, %s, %s )", fields)
        #
        # mydb.commit()
