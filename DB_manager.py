import mysql.connector
import config


class DBManager:

    def __init__(self):
        try:
            self.welfare_db = mysql.connector.connect(host=config.HOST,
                                                      user=config.USERNAME,
                                                      passwd=config.PASSWORD)
        except (TypeError, ValueError, ConnectionError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()
        self.cur = self.welfare_db.cursor()

    def connect_to_DB(self):
        self.cur.execute(f'DROP DATABASE IF EXISTS {config.DATABASE_NAME}')
        self.cur.execute(f'CREATE DATABASE {config.DATABASE_NAME}')
        self.cur.execute(f'USE {config.DATABASE_NAME}')
        config.logger.info(f'Connected to DB "{config.DATABASE_NAME}"')

    def setup_DB(self):
        self._create_table_countries()
        years = list(map(str, range(2010, config.CURRENT_YEAR)))
        for year in years:
            self._create_table_property_price(year)
        config.logger.info(f'Finished setting up DB "{config.DATABASE_NAME}"')

    def close_DB(self):
        self.welfare_db.close()

    def _create_table_countries(self):
        self.cur.execute('''CREATE TABLE countries( country_id INT AUTO_INCREMENT PRIMARY KEY,
                                                    country_name VARCHAR(255))''')
        self.welfare_db.commit()
        query = "INSERT INTO countries (country_name) VALUES (%s)"
        countries_list_tuples = [(country, ) for country in config.countries_list]
        self.cur.executemany(query, countries_list_tuples)
        self.welfare_db.commit()
        config.logger.info('Created table "countries"')

    def _create_table_property_price(self, year):
        subject = config.WelfareType.property_investment.value
        table_name = f'{subject}_{year}'
        if table_name not in config.countries_data:
            return
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
        for row in config.countries_data[f'{subject}_{year}'][1:]:
            fields = [dic_country, year, *row[1:]]
            self.cur.execute('''INSERT INTO property_price 
                                            (country_id, 
                                            year, 
                                            price_to_income, 
                                            gross_rental_inside_center, 
                                            gross_rental_outside_center, 
                                            price_rent_city_center, 
                                            price_rent_outside_city_center,
                                            mortgage_as_prc_income, 
                                            affordability) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', fields)
