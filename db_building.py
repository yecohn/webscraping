import sqlite3
import os
import welfare_data
import datetime
DATABASE_NAME= 'parser.db'

if os.path.exists(DATABASE_NAME):
   os.remove(DATABASE_NAME)


with sqlite3.connect(DATABASE_NAME) as con:
    cur = con.cursor()
    cur.execute('''CREATE TABLE  property_price(
                       year INT,
                       country VARCHAR,
                       price_to_income FLOAT,
                       gross_rental_inside_center FLOAT,
                       gross_rental_outside_center FLOAT,
                       price_rent_city_center FLOAT,
                       price_rent_outside_city_center FLOAT,
                       mortgage_as_prc_income FLOAT,
                       affordability FLOAT,
                       PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'property-investment'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
       for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
            fields = [year, *row]
            cur.execute("INSERT INTO property_price (year, country, price_to_income, gross_rental_inside_center, gross_rental_outside_center, \
                           price_rent_city_center, \
                           price_rent_outside_city_center, mortgage_as_prc_income, affordability) VALUES \
                           (?, ?, ?, ?, ?, ?, ?, ?, ?)", fields)
            con.commit()
    con.commit()
    cur.execute('''CREATE TABLE  cost_of_living(
                               year INT,
                               country VARCHAR,
                               cost_of_living FLOAT,
                               rent FLOAT,
                               cost_of_living_and_rent FLOAT,
                               groceries_prices FLOAT,
                               restaurant_prices FLOAT,
                               local_purchasing_power FLOAT,
                               PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'cost-of-living'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
        for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
           fields = [year, *row]
           cur.execute("INSERT INTO cost_of_living (year, country, cost_of_living, rent, cost_of_living_and_rent, \
                                   groceries_prices, restaurant_prices, local_purchasing_power) VALUES \
                                   (?, ?, ?, ?, ?, ?, ?, ?)", fields)
        con.commit()
    con.commit()
    cur.execute('''CREATE TABLE  traffic(
                               year INT,
                               country VARCHAR,
                               traffic_id FLOAT,
                               time_id FLOAT,
                               time_exp_id, FLOAT,
                               inefficiency_id FLOAT,
                               CO2_emission_id FLOAT,
                               PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'traffic'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
        for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
           fields = [year, *row]
           cur.execute("INSERT INTO traffic (year, country, traffic_id, time_id, time_exp_id, inefficiency_id , \
                                   CO2_emission_id) VALUES \
                                   (?, ?, ?, ?, ?, ?, ?)", fields)
        con.commit()
    con.commit()

    cur.execute('''CREATE TABLE  health_care(
                              year INT,
                              country VARCHAR,
                              health_care_id FLOAT,
                              health_care_exp_id FLOAT,
                                PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'health-care'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
        for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
            fields = [year, *row]
            cur.execute("INSERT INTO health_care (year, country, health_care_id, health_care_exp_id) VALUES \
                                    (?, ?, ?, ?)", fields)

            con.commit()
    con.commit()

    cur.execute('''CREATE TABLE  pollution(
                                year INT,
                                country VARCHAR,
                                pollution_id,
                                exp_pollution_id,
                                PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'pollution'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
        for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
            fields = [year, *row]
            cur.execute("INSERT INTO pollution (year, country, pollution_id, exp_pollution_id) VALUES \
                                    (?, ?, ?, ?)", fields)

            con.commit()
    con.commit()

    cur.execute('''CREATE TABLE  quality_life(
                                year INT,
                                country VARCHAR,
                                quality_life_id FLOAT,
                                purchase_power_id FLOAT,
                                safety_id FLOAT,
                                health_care_id FLOAT,
                                cost_living_id FLOAT,
                                property_price_to_income_id FLOAT,
                                traffic_commute_time_id FLOAT,
                                pollution_id FLOAT,
                                climate_id FLOAT,
                                PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'quality-of-life'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
        for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
            fields = [year, *row]
            cur.execute("INSERT INTO quality_life (year, country, quality_life_id, purchase_power_id, safety_id, \
                                    health_care_id, cost_living_id, property_price_to_income_id, \
                                    traffic_commute_time_id, pollution_id, climate_id) VALUES \
                                     (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fields)

            con.commit()
    con.commit()

    cur.execute('''CREATE TABLE  crime(
                                year INT,
                                country VARCHAR,
                                crime_id FLOAT,
                                safety_id FLOAT,
                                PRIMARY KEY (year, country))''')
    SUBJECT_NAME = 'crime'
    CURRENT_YEAR = int(datetime.datetime.now().year)
    YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
    for year in YEARS:
            for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
                fields = [year, *row]
                cur.execute("INSERT INTO crime (year, country, crime_id, safety_id) VALUES \
                                    (?, ?, ?, ? )", fields)

                con.commit()
    con.commit()
    cur.close()



