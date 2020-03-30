

import os
import welfare_data
import datetime
import mysql.connector
from _collections import defaultdict
DATABASE_NAME= 'parser'
HOST = 'localhost'
USERNAME = 'root'
PASSWD= 'azerty051210'

try:
    mydb = mysql.connector.connect(host=HOST,
                               user =USERNAME,
                               passwd =PASSWD,
                               database =DATABASE_NAME)

    cur = mydb.cursor()
except:
    mydb = mysql.connector.connect(host=HOST,
                                   user=USERNAME,
                                   passwd=PASSWD,
                                   )

    cur = mydb.cursor()
    cur.execute("CREATE DATABASE parser")

cur.execute('''DROP TABLE IF EXISTS property_price''')
cur.execute('''DROP TABLE IF EXISTS cost_of_living''')
cur.execute('''DROP TABLE IF EXISTS traffic''')
cur.execute('''DROP TABLE IF EXISTS pollution''')
cur.execute('''DROP TABLE IF EXISTS health_care''')
cur.execute('''DROP TABLE IF EXISTS quality_life''')
cur.execute('''DROP TABLE IF EXISTS crime''')
cur.execute('''DROP TABLE IF EXISTS countries''')

mydb.commit()





cur.execute('''CREATE TABLE countries(
                                    country_id  INT AUTO_INCREMENT PRIMARY KEY,
                                    country_name VARCHAR(255))''')
mydb.commit()



with open('country_list.csv', 'r') as f1:
    list_country = f1.read().replace('\n', '').split(',')
    dic_country = defaultdict(int)
    counter = 1
for cont in list_country:
    dic_country[cont] = counter
    counter += 1




for row in list_country :
    cur.execute("INSERT INTO countries (country_name) VALUES (%s)", (row,))

mydb.commit()


cur.execute('''CREATE TABLE  property_price(
                       id  INT PRIMARY KEY AUTO_INCREMENT,
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


SUBJECT_NAME = 'property-investment'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO property_price (country_id, year, price_to_income, gross_rental_inside_center, gross_rental_outside_center, \
                           price_rent_city_center, \
                           price_rent_outside_city_center, mortgage_as_prc_income, affordability) VALUES \
                           (%s, %s, %s, %s, %s, %s, %s, %s, %s)", fields)

mydb.commit()
cur.execute('''CREATE TABLE  cost_of_living(
                               id  INT PRIMARY KEY AUTO_INCREMENT,
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
SUBJECT_NAME = 'cost-of-living'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO cost_of_living (country_id, year, cost_of_living, rent, cost_of_living_and_rent, \
                                   groceries_prices, restaurant_prices, local_purchasing_power) VALUES \
                                   (%s, %s, %s, %s, %s, %s, %s, %s)", fields)
mydb.commit()

cur.execute('''CREATE TABLE  traffic(
                               id  INT PRIMARY KEY AUTO_INCREMENT,
                               country_id INT,
                               year INT,
                               traffic_id FLOAT,
                               time_id FLOAT,
                               time_exp_id FLOAT,
                               inefficiency_id FLOAT,
                               CO2_emission_id FLOAT,
                               foreign key (country_id) references countries(country_id)
                               )''')
SUBJECT_NAME = 'traffic'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO traffic (country_id, year, traffic_id, time_id, time_exp_id, inefficiency_id , \
                                   CO2_emission_id) VALUES \
                                   (%s, %s, %s, %s, %s, %s, %s)", fields)

mydb.commit()

cur.execute('''CREATE TABLE  health_care(
                                id  INT PRIMARY KEY AUTO_INCREMENT, 
                                country_id INT,
                                year INT,  
                                health_care_id FLOAT,
                                health_care_exp_id FLOAT,
                                foreign key (country_id) references countries(country_id)
                                )''')
SUBJECT_NAME = 'health-care'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO health_care (country_id, year,health_care_id, health_care_exp_id) VALUES \
                                    (%s,%s, %s, %s)", fields)


mydb.commit()

cur.execute('''CREATE TABLE  pollution(
                                id  INT PRIMARY KEY AUTO_INCREMENT, 
                                country_id INT,
                                year INT,
                                pollution_id INT,
                                exp_pollution_id INT,
                                foreign key (country_id) references countries(country_id)
                                )''')
SUBJECT_NAME = 'pollution'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO pollution (country_id, year, pollution_id, exp_pollution_id) VALUES \
                                    (%s ,%s, %s, %s)", fields)

mydb.commit()


cur.execute('''CREATE TABLE  quality_life(
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
                                foreign key (country_id) references countries(country_id)
                                )''')
SUBJECT_NAME = 'quality-of-life'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]
for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year,   SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()

        cur.execute("INSERT INTO quality_life (country_id, year, quality_life_id, purchase_power_id, safety_id, \
                                    health_care_id, cost_living_id, property_price_to_income_id, \
                                    traffic_commute_time_id, pollution_id, climate_id) VALUES \
                                     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", fields)


mydb.commit()

cur.execute('''CREATE TABLE  crime(
                                id  INT PRIMARY KEY AUTO_INCREMENT, 
                                country_id INT, 
                                year INT,
                                crime_id FLOAT,
                                safety_id FLOAT,
                                foreign key (country_id) references countries(country_id)
                                )''')
SUBJECT_NAME = 'crime'
CURRENT_YEAR = int(datetime.datetime.now().year)
YEARS = [str(year) for year in range(2010, CURRENT_YEAR + 1)]

for year in YEARS:
    for row in welfare_data.log_ranking(SUBJECT_NAME, year)[1:]:
        if row[0] in dic_country:
            print('the country: {} for year: {} is being added to table {}'.format(row[0], year, SUBJECT_NAME))
            fields = [dic_country[row[0]], year, *row[1:]]
        else:
            dic_country[row[0]] = counter
            counter += 1
            fields = [dic_country[row[0]], year, *row[1:]]
            cur.execute('INSERT INTO countries(country_name) VALUES (%s)', (row[0],))
            mydb.commit()
        cur.execute("INSERT INTO crime (country_id, year, crime_id, safety_id) VALUES \
                                    (%s, %s, %s, %s )", fields)

mydb.commit()





