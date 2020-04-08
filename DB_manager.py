import mysql.connector
import config


class DBManager:

    def __init__(self):
        try:
            config.logger.info(f'Started connecting to DB "{config.DATABASE_NAME}"')
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
        config.logger.info(f'Finished connecting to DB "{config.DATABASE_NAME}"')

    def setup_DB(self):
        config.logger.info(f'Started setting up DB "{config.DATABASE_NAME}"')
        self._create_table_countries()
        years = list(range(2010, config.CURRENT_YEAR))
        for year in years:
            self._create_table_property_price(year)
            self._create_table_cost_of_living(year)
            #self._create_table_crime(year)
        config.logger.info(f'Finished setting up DB "{config.DATABASE_NAME}"')

    def close_DB(self):
        self.welfare_db.close()

    @staticmethod
    def _get_fields(row, year):
        country_name = row[0]
        if country_name not in config.countries_dict:
            return None
        return (config.countries_dict[country_name], year, *row[1:])

    def _create_table_countries(self):
        self.cur.execute('''CREATE TABLE countries( country_id INT PRIMARY KEY,
                                                    country_name VARCHAR(255))''')
        self.welfare_db.commit()
        query = "INSERT INTO countries (country_id, country_name) VALUES (%s, %s)"
        countries_list = [(country_id, country_name) for country_name, country_id in config.countries_dict.items()]
        self.cur.executemany(query, countries_list)
        self.welfare_db.commit()
        config.logger.info('Created table "countries"')

    def _create_table_property_price(self, year):
        subject = config.WelfareType.property_investment.value
        table_name = f'{subject}_{year}'
        if table_name not in list(config.countries_data.keys()):
            return
        self.cur.execute('''CREATE TABLE property_price(
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
        for row in config.countries_data[table_name][1:]:
            fields = DBManager._get_fields(row, year)
            if fields is None:
                continue
            self.cur.execute('''INSERT INTO property_price (
                                                            country_id, 
                                                            year, 
                                                            price_to_income, 
                                                            gross_rental_inside_center, 
                                                            gross_rental_outside_center, 
                                                            price_rent_city_center, 
                                                            price_rent_outside_city_center,
                                                            mortgage_as_prc_income, 
                                                            affordability) 
                                                            
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', fields)
            self.welfare_db.commit()
        config.logger.info(f'Created table "{table_name}"')

    def _create_table_cost_of_living(self, year):
        subject = config.WelfareType.cost_of_living.value
        table_name = f'{subject}_{year}'
        if table_name not in list(config.countries_data.keys()):
            return
        self.cur.execute('''CREATE TABLE cost_of_living(
                                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                                        country_id INT,
                                                        year INT,
                                                        cost_of_living FLOAT,
                                                        rent FLOAT,
                                                        cost_of_living_and_rent FLOAT,
                                                        groceries_prices FLOAT,
                                                        restaurant_prices FLOAT,
                                                        local_purchasing_power FLOAT,
                                                        FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                        )''')
        self.welfare_db.commit()
        for row in config.countries_data[table_name][1:]:
            fields = DBManager._get_fields(row, year)
            if fields is None:
                continue
            self.cur.execute('''INSERT INTO cost_of_living (
                                                            country_id,
                                                            year,
                                                            cost_of_living,
                                                            rent,
                                                            cost_of_living_and_rent,
                                                            groceries_prices,
                                                            restaurant_prices,
                                                            local_purchasing_power)

                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', fields)
        config.logger.info(f'Created table "{table_name}"')
    #
    # def _create_table_crime(self, year):
    #     subject = config.WelfareType.cost_of_living.value
    #     table_name = f'{subject}_{year}'
    #     if table_name not in list(config.countries_data.keys()):
    #         return
    #     self.cur.execute('''CREATE TABLE  crime(
    #             #                                 id INT PRIMARY KEY AUTO_INCREMENT,
    #             #                                 country_id INT,
    #             #                                 year INT,
    #             #                                 crime_id FLOAT,
    #             #                                 safety_id FLOAT,
    #             #                                 foreign key (country_id) references countries(country_id)
    #             #                                 )''')
    #     self.welfare_db.commit()
    #     for row in config.countries_data[table_name][1:]:
    #         fields = DBManager._get_fields(row, year)
    #         if fields is None:
    #             continue
    #         self.cur.execute('''INSERT INTO cost_of_living (
    #                                                         country_id,
    #                                                         year,
    #                                                         cost_of_living,
    #                                                         rent,
    #                                                         cost_of_living_and_rent,
    #                                                         groceries_prices,
    #                                                         restaurant_prices,
    #                                                         local_purchasing_power)
    #
    #                                                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', fields)
    #     config.logger.info(f'Created table "{table_name}"')