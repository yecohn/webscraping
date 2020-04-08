import mysql.connector
import config


class DBManager:

    def __init__(self):
        config.logger.info(f'Started connecting to DB "{config.DATABASE_NAME}"')
        try:
            self.welfare_db = mysql.connector.connect(host=config.HOST,
                                                      user=config.USERNAME,
                                                      passwd=config.PASSWORD)
        except (TypeError, ValueError, ConnectionError, Exception) as e:
            config.logger.critical(e, exc_info=True)
            config.exit_program()
        self.cur = self.welfare_db.cursor()

    def setup_DB(self):
        config.logger.info(f'Started setting up DB "{config.DATABASE_NAME}"')
        self._create_table_countries()
        years = list(range(2010, config.CURRENT_YEAR))
        welfare_types = [welfare_type.value.replace('-', '_') for welfare_type in config.WelfareType]
        for year in years:
            for welfare_type in welfare_types:
                eval(f'self._create_table_{welfare_type}({year})')
        config.logger.info(f'Finished setting up DB "{config.DATABASE_NAME}"')

    def connect_to_DB(self):
        self.cur.execute(f'CREATE DATABASE IF NOT EXISTS {config.DATABASE_NAME}')
        self.cur.execute(f'USE {config.DATABASE_NAME}')
        config.logger.info(f'Finished connecting to DB "{config.DATABASE_NAME}"')

    def close_DB(self):
        self.welfare_db.close()

    def _create_table(self, subject, year, create_table_query, insert_into_query):
        data_name = f'{subject}_{year}'
        if data_name not in list(config.countries_data.keys()):
            return
        self.cur.execute(create_table_query)
        self.welfare_db.commit()
        for row in config.countries_data[data_name][1:]:
            country_name = row[0]
            if country_name not in config.countries_dict:
                continue
            fields = (config.countries_dict[country_name], year, *row[1:])
            if fields is None:
                continue
            self.cur.execute(insert_into_query, fields)
            self.welfare_db.commit()
        config.logger.info(f'Created table "{subject}"')

    def _create_table_countries(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS countries(country_id INT PRIMARY KEY,
                                                                country_name VARCHAR(255))''')
        self.welfare_db.commit()
        query = "INSERT INTO countries (country_id, country_name) VALUES (%s, %s)"
        countries_list = [(country_id, country_name) for country_name, country_id in config.countries_dict.items()]
        self.cur.executemany(query, countries_list)
        self.welfare_db.commit()
        config.logger.info('Created table "countries"')

    def _create_table_property_investment(self, year):
        subject = config.WelfareType.property_investment.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS property_investment(
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
                                                            )
                                '''
        insert_into_query = '''
                                INSERT INTO property_investment (
                                                            country_id, 
                                                            year, 
                                                            price_to_income, 
                                                            gross_rental_inside_center, 
                                                            gross_rental_outside_center, 
                                                            price_rent_city_center, 
                                                            price_rent_outside_city_center,
                                                            mortgage_as_prc_income, 
                                                            affordability) 
                                                        
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_cost_of_living(self, year):
        subject = config.WelfareType.cost_of_living.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS cost_of_living(
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
                                                        )
                                '''
        insert_into_query = '''
                                INSERT INTO cost_of_living (
                                                            country_id,
                                                            year,
                                                            cost_of_living,
                                                            rent,
                                                            cost_of_living_and_rent,
                                                            groceries_prices,
                                                            restaurant_prices,
                                                            local_purchasing_power)

                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_crime(self, year):
        subject = config.WelfareType.crime.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS crime(
                                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                                    country_id INT,
                                                    year INT,
                                                    crime_id FLOAT,
                                                    safety_id FLOAT,
                                                    FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                    )
                                '''
        insert_into_query = '''
                                INSERT INTO crime (  
                                                    country_id, 
                                                    year, 
                                                    crime_id, 
                                                    safety_id) 
                                                    VALUES (%s, %s, %s, %s )
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_quality_of_life(self, year):
        subject = config.WelfareType.quality_of_life.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS quality_life(
                                                            id  INT PRIMARY KEY AUTO_INCREMENT,
                                                            country_id INT,
                                                            year INT,
                                                            quality_life_id FLOAT,
                                                            purchase_power_id FLOAT,
                                                            safety_id FLOAT,
                                                            health_care_id FLOAT,
                                                            cost_living_id FLOAT,
                                                            property_price_to_income_id FLOAT,
                                                            traffic_commute_time_id FLOAT,
                                                            pollution_id FLOAT,
                                                            climate_id VARCHAR(255),
                                                            FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                            )
                                '''
        insert_into_query = '''
                                INSERT INTO quality_life (  country_id, 
                                                            year, 
                                                            quality_life_id, 
                                                            purchase_power_id, 
                                                            safety_id,
                                                            health_care_id, 
                                                            cost_living_id, 
                                                            property_price_to_income_id,
                                                            traffic_commute_time_id, 
                                                            pollution_id, 
                                                            climate_id)
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_pollution(self, year):
        subject = config.WelfareType.pollution.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS pollution(
                                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                                        country_id INT,
                                                        year INT,
                                                        pollution_id INT,
                                                        exp_pollution_id INT,
                                                        FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                        )
                            '''
        insert_into_query = '''
                                INSERT INTO pollution (
                                                        country_id, 
                                                        year, 
                                                        pollution_id, 
                                                        exp_pollution_id
                                                        ) 
                                                        VALUES (%s ,%s, %s, %s)
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_health_care(self, year):
        subject = config.WelfareType.health_care.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS health_care(
                                                            id INT PRIMARY KEY AUTO_INCREMENT,
                                                            country_id INT,
                                                            year INT,
                                                            health_care_id FLOAT,
                                                            health_care_exp_id FLOAT,
                                                            FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                            )
                            '''
        insert_into_query = '''
                                    INSERT INTO health_care (
                                                            country_id, 
                                                            year,
                                                            health_care_id, 
                                                            health_care_exp_id
                                                            ) 
                                                            VALUES (%s,%s, %s, %s)
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)

    def _create_table_traffic(self, year):
        subject = config.WelfareType.traffic.value
        create_table_query = '''
                                CREATE TABLE IF NOT EXISTS traffic(
                                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                                        country_id INT,
                                                        year INT,
                                                        traffic_id FLOAT,
                                                        time_id FLOAT,
                                                        time_exp_id FLOAT,
                                                        inefficiency_id FLOAT,
                                                        CO2_emission_id FLOAT,
                                                        FOREIGN KEY (country_id) REFERENCES countries(country_id)
                                                    )
                            '''
        insert_into_query = '''
                                INSERT INTO traffic (
                                                    country_id, 
                                                    year, 
                                                    traffic_id, 
                                                    time_id, 
                                                    time_exp_id, 
                                                    inefficiency_id,
                                                    CO2_emission_id
                                                    )
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                            '''
        self._create_table(subject, year, create_table_query, insert_into_query)
