"""
    Global variables to be accessed from all of the project
"""

import logging
import enum
import sys
import collections
import datetime
import pprint


countries_dict = {'Norway': 1, 'Switzerland': 2, 'Denmark': 3, 'Venezuela': 4, 'Iceland': 5, 'Luxembourg': 6, 'Australia': 7, 'Ireland': 8, 'New Zealand': 9, 'Sweden': 10, 'Bahamas': 11, 'Finland': 12, 'France': 13, 'United Kingdom': 14, 'Belgium': 15, 'Singapore': 16, 'Netherlands': 17, 'Italy': 18, 'Japan': 19, 'Israel': 20, 'Cyprus': 21, 'Austria': 22, 'Canada': 23, 'South Korea': 24, 'Germany': 25, 'Greece': 26, 'Malta': 27, 'United States': 28, 'Uruguay': 29, 'Spain': 30, 'Puerto Rico': 31, 'Hong Kong': 32, 'Slovenia': 33, 'Qatar': 34, 'Kuwait': 35, 'Nigeria': 36, 'Jamaica': 37, 'Lebanon': 38, 'Zimbabwe': 39, 'Portugal': 40, 'Croatia': 41, 'United Arab Emirates': 42, 'Saudi Arabia': 43, 'Estonia': 44, 'Argentina': 45, 'Latvia': 46, 'Costa Rica': 47, 'Ghana': 48, 'Kazakhstan': 49, 'Azerbaijan': 50, 'Russia': 51, 'Slovakia': 52, 'Jordan': 53, 'Brazil': 54, 'Taiwan': 55, 'Chile': 56, 'Lithuania': 57, 'Namibia': 58, 'Mauritius': 59, 'Hungary': 60, 'Bahrain': 61, 'Trinidad And Tobago': 62, 'Uganda': 63, 'Dominican Republic': 64, 'Montenegro': 65, 'Czech Republic': 66, 'Oman': 67, 'Ethiopia': 68, 'China': 69, 'Poland': 70, 'Cambodia': 71, 'Kenya': 72, 'El Salvador': 73, 'Libya': 74, 'Panama': 75, 'Guatemala': 76, 'Serbia': 77, 'Iraq': 78, 'Honduras': 79, 'Peru': 80, 'Colombia': 81, 'Belarus': 82, 'Tanzania': 83, 'Bulgaria': 84, 'Turkey': 85, 'Bosnia And Herzegovina': 86, 'Iran': 87, 'Albania': 88, 'Malaysia': 89, 'South Africa': 90, 'Romania': 91, 'Morocco': 92, 'Mexico': 93, 'Armenia': 94, 'Georgia': 95, 'Thailand': 96, 'Ukraine': 97, 'Ecuador': 98, 'Vietnam': 99, 'North Macedonia': 100, 'Sri Lanka': 101, 'Syria': 102, 'Moldova': 103, 'Tunisia': 104, 'Bolivia': 105, 'Bangladesh': 106, 'Philippines': 107, 'Algeria': 108, 'Indonesia': 109, 'Egypt': 110, 'Nepal': 111, 'Pakistan': 112, 'India': 113}
countries_data = collections.defaultdict(list, {'cost-of-living_2013': [['Country', 'Cost of Living Index', 'Rent Index', 'Cost of Living Plus Rent Index', 'Groceries Index', 'Restaurant Price Index', 'Local Purchasing Power Index'], ['Norway', '173.85', '68.99', '123.52', '162.53', '183.30', '95.91'], ['Switzerland', '151.77', '70.90', '112.95', '153.05', '142.36', '137.26'], ['Australia', '133.66', '72.72', '104.41', '128.69', '116.39', '103.02'], ['Luxembourg', '124.76', '67.68', '97.36', '111.78', '130.80', '121.39'], ['Denmark', '119.95', '42.93', '82.98', '103.97', '130.50', '102.15'], ['Japan', '115.24', '43.81', '80.96', '112.83', '70.01', '85.99'], ['Sweden', '114.47', '36.11', '76.86', '105.57', '110.14', '106.57'], ['New Zealand', '113.63', '46.06', '81.20', '111.68', '93.48', '80.65'], ['Bahrain', '113.49', '29.58', '73.21', '162.91', '71.01', '59.29'], ['Iceland', '112.43', '39.30', '77.33', '118.81', '99.72', '67.91'], ['Ireland', '112.33', '40.37', '77.79', '105.55', '102.99', '95.06'], ['Venezuela', '111.01', '41.48', '77.64', '126.37', '93.65', '16.64'], ['Belgium', '108.04', '39.18', '74.99', '90.14', '115.60', '94.09'], ['Finland', '106.99', '40.37', '75.02', '101.29', '100.24', '94.06'], ['Singapore', '105.39', '103.04', '104.26', '91.19', '63.28', '59.94'], ['Netherlands', '103.90', '45.71', '75.97', '81.11', '107.68', '92.88'], ['France', '103.24', '37.99', '71.92', '97.75', '100.45', '98.11'], ['United Kingdom', '102.24', '41.10', '72.89', '93.06', '94.28', '89.07'], ['Italy', '101.42', '36.21', '70.12', '87.31', '107.38', '70.44'], ['Canada', '99.65', '39.85', '70.94', '101.24', '85.58', '109.56'], ['Cyprus', '98.61', '24.99', '63.28', '89.35', '101.17', '72.48'], ['Austria', '97.88', '36.81', '68.57', '92.75', '81.43', '87.47'], ['Greece', '92.57', '18.64', '57.09', '74.67', '95.52', '49.44'], ['Israel', '92.24', '32.28', '63.46', '76.92', '90.09', '72.55'], ['Germany', '91.64', '33.24', '63.61', '80.74', '79.68', '117.58'], ['Nigeria', '87.18', '17.89', '53.92', '92.93', '62.45', '32.73'], ['Malta', '85.61', '20.60', '54.40', '73.68', '77.57', '77.82'], ['Spain', '83.14', '29.09', '57.20', '66.55', '80.97', '84.04'], ['Puerto Rico', '82.56', '25.00', '54.93', '83.45', '65.03', '94.08'], ['Qatar', '82.36', '84.11', '83.20', '75.00', '78.79', '136.65'], ['Slovenia', '82.06', '26.48', '55.38', '70.49', '63.24', '59.25'], ['Uruguay', '81.66', '26.14', '55.01', '70.53', '75.66', '37.58'], ['Kuwait', '80.74', '34.55', '58.57', '78.99', '78.65', '84.61'], ['United States', '80.54', '37.39', '59.83', '80.74', '67.87', '136.50'], ['South Korea', '80.44', '28.66', '55.58', '94.12', '46.50', '102.13'], ['Azerbaijan', '78.25', '41.92', '60.81', '67.88', '64.83', '20.48'], ['Hong Kong', '77.81', '88.57', '82.98', '79.82', '54.48', '80.30'], ['Lebanon', '75.63', '38.51', '57.82', '58.06', '65.20', '42.46'], ['United Arab Emirates', '75.48', '63.29', '69.63', '64.99', '69.90', '121.24'], ['Portugal', '75.31', '24.34', '50.84', '61.25', '59.09', '54.12'], ['Croatia', '72.24', '14.90', '44.72', '64.47', '55.98', '51.58'], ['Saudi Arabia', '72.17', '15.73', '45.08', '74.47', '36.51', '114.63'], ['Estonia', '70.75', '16.80', '44.86', '60.94', '53.36', '53.09'], ['Argentina', '70.44', '20.12', '46.29', '64.52', '65.43', '50.24'], ['Brazil', '70.00', '22.79', '47.34', '53.97', '51.81', '41.26'], ['Russia', '69.69', '29.38', '50.34', '56.88', '73.64', '42.96'], ['Chile', '68.38', '21.30', '45.79', '58.15', '56.28', '56.43'], ['Latvia', '67.96', '15.26', '42.67', '55.36', '58.45', '41.34'], ['Taiwan', '67.83', '20.52', '45.12', '79.96', '31.75', '73.02'], ['Costa Rica', '66.62', '20.87', '44.66', '71.79', '54.70', '45.59'], ['Dominican Republic', '66.17', '15.44', '41.82', '66.12', '41.54', '27.99'], ['Slovakia', '65.72', '24.46', '45.92', '56.16', '44.54', '53.78'], ['Jordan', '65.55', '15.63', '41.59', '56.78', '56.37', '36.18'], ['Kazakhstan', '65.16', '26.56', '46.64', '51.34', '67.36', '32.21'], ['Turkey', '64.39', '16.16', '41.24', '50.04', '46.33', '56.44'], ['Hungary', '63.90', '12.60', '39.28', '50.87', '47.33', '42.97'], ['Czech Republic', '63.35', '21.04', '43.04', '54.69', '40.61', '60.65'], ['Lithuania', '63.33', '16.18', '40.70', '55.36', '41.98', '42.24'], ['Montenegro', '63.18', '15.20', '40.15', '56.02', '55.20', '43.94'], ['China', '61.75', '25.82', '44.51', '66.43', '36.53', '37.27'], ['Trinidad And Tobago', '61.60', '30.56', '46.70', '55.80', '48.42', '44.27'], ['South Africa', '60.20', '21.39', '41.57', '52.86', '49.76', '105.33'], ['Ethiopia', '59.86', '24.26', '42.77', '62.51', '26.10', '11.48'], ['Colombia', '58.44', '14.01', '37.12', '52.83', '38.31', '29.71'], ['Iraq', '57.16', '18.04', '38.39', '50.89', '46.23', '33.66'], ['Iran', '57.04', '24.30', '41.33', '59.28', '42.76', '37.51'], ['Kenya', '56.99', '17.19', '37.89', '60.96', '33.82', '38.93'], ['Cambodia', '55.84', '9.18', '33.44', '64.35', '24.45', '15.45'], ['Poland', '55.64', '20.20', '38.63', '46.58', '43.08', '54.72'], ['Tanzania', '54.88', '13.91', '35.22', '59.20', '24.94', '66.03'], ['Malaysia', '54.82', '15.25', '35.83', '51.46', '27.37', '69.64'], ['Oman', '54.56', '27.50', '41.57', '51.37', '39.81', '129.20'], ['Mauritius', '54.48', '23.36', '39.54', '43.46', '53.48', '46.08'], ['Morocco', '54.04', '16.70', '36.12', '44.71', '42.31', '26.38'], ['Georgia', '53.80', '17.09', '36.18', '45.54', '47.48', '28.56'], ['Serbia', '53.59', '11.96', '33.61', '43.53', '42.78', '36.58'], ['Mexico', '53.56', '13.29', '34.23', '52.48', '37.40', '59.77'], ['Bosnia And Herzegovina', '53.40', '8.65', '31.92', '47.43', '38.07', '46.42'], ['Panama', '53.38', '28.26', '41.32', '58.83', '36.26', '37.52'], ['Bulgaria', '52.68', '12.39', '33.35', '46.89', '38.82', '37.71'], ['Romania', '51.89', '14.14', '33.77', '47.31', '37.20', '35.81'], ['Thailand', '51.78', '21.30', '37.15', '57.93', '25.48', '35.01'], ['Belarus', '51.32', '13.28', '33.06', '41.89', '58.09', '23.45'], ['Sri Lanka', '50.58', '14.52', '33.27', '55.00', '29.73', '27.18'], ['Tunisia', '50.32', '11.61', '31.74', '44.39', '36.83', '34.18'], ['Peru', '48.82', '15.47', '32.81', '42.62', '31.18', '45.28'], ['Albania', '48.64', '10.84', '30.50', '40.23', '31.83', '35.28'], ['Ukraine', '48.56', '14.74', '32.33', '41.48', '43.47', '31.97'], ['Philippines', '48.01', '10.91', '30.20', '51.23', '26.89', '25.66'], ['Syria', '47.30', '17.61', '33.05', '36.70', '40.65', '21.89'], ['Moldova', '47.24', '12.89', '30.75', '38.28', '37.97', '24.52'], ['Ecuador', '46.61', '12.91', '30.44', '48.18', '26.45', '25.47'], ['North Macedonia', '46.48', '10.72', '29.32', '38.44', '33.22', '34.90'], ['Indonesia', '46.14', '17.58', '32.43', '51.00', '23.71', '24.62'], ['Bangladesh', '44.83', '7.79', '27.05', '38.51', '26.43', '33.26'], ['Egypt', '44.82', '11.10', '28.64', '40.33', '37.18', '30.32'], ['Vietnam', '43.21', '20.77', '32.44', '41.77', '23.74', '31.86'], ['Bolivia', '41.50', '12.48', '27.57', '36.42', '21.48', '46.39'], ['Algeria', '41.49', '6.06', '24.48', '43.76', '24.84', '32.71'], ['Nepal', '38.74', '3.66', '21.91', '36.73', '26.19', '29.49'], ['Pakistan', '33.41', '6.12', '20.31', '32.09', '25.34', '26.03'], ['India', '30.92', '7.36', '19.61', '32.51', '18.09', '61.92']], 'crime_2010': [['Country', 'Crime Index', 'Safety Index']], 'health-care_2012': [['Country', 'Health Care Index', 'Health CareExp. Index']], 'pollution_2015': [['Country', 'Pollution Index', 'Exp Pollution Index'], ['Senegal', '110.34', '206.09'], ['Ghana', '109.27', '200.44'], ['Afghanistan', '100.34', '184.06'], ['Iraq', '96.72', '177.24'], ['Egypt', '96.62', '175.65'], ['Liberia', '95.29', '179.52'], ['Mongolia', '94.55', '175.75'], ['Bolivia', '94.05', '170.03'], ['Bangladesh', '93.59', '169.25'], ['China', '89.36', '164.03'], ['Lebanon', '89.11', '159.76'], ['Yemen', '88.53', '162.14'], ['Myanmar', '87.89', '161.66'], ['Qatar', '87.73', '158.95'], ['El Salvador', '87.52', '158.80'], ['Bahrain', '87.36', '159.86'], ['Peru', '86.50', '155.45'], ['Jordan', '85.64', '152.71'], ['Botswana', '85.06', '153.78'], ['Vietnam', '84.34', '149.78'], ['Pakistan', '83.73', '149.37'], ['Nepal', '83.39', '148.44'], ['North Macedonia', '82.31', '155.23'], ['Iran', '82.28', '150.90'], ['Azerbaijan', '81.30', '146.01'], ['Trinidad And Tobago', '80.15', '142.73'], ['Cambodia', '80.06', '143.96'], ['Venezuela', '79.19', '141.24'], ['India', '77.72', '137.41'], ['Jamaica', '77.20', '136.84'], ['South Korea', '77.11', '140.95'], ['Nigeria', '76.29', '134.27'], ['Albania', '76.21', '134.11'], ['Zambia', '76.12', '149.07'], ['Honduras', '75.20', '135.16'], ['Indonesia', '74.41', '130.40'], ['Turkey', '74.31', '131.19'], ['Philippines', '74.17', '130.17'], ['Kazakhstan', '73.69', '134.68'], ['Tunisia', '73.54', '130.02'], ['Armenia', '73.03', '134.85'], ['Thailand', '72.81', '126.72'], ['Russia', '72.77', '128.20'], ['Chile', '72.40', '132.62'], ['Maldives', '71.89', '125.23'], ['Guatemala', '71.14', '124.03'], ['Saudi Arabia', '71.02', '125.44'], ['Ukraine', '69.85', '122.71'], ['Monaco', '68.89', '125.29'], ['Mexico', '68.83', '119.56'], ['Laos', '68.56', '120.32'], ['Algeria', '68.37', '119.61'], ['Taiwan', '67.65', '119.94'], ['Tanzania', '66.78', '115.55'], ['Ethiopia', '66.74', '119.68'], ['Zimbabwe', '65.86', '118.73'], ['Sri Lanka', '65.72', '114.62'], ['Greenland', '65.52', '118.58'], ['Dominican Republic', '65.32', '113.00'], ['Israel', '65.21', '116.35'], ['South Africa', '65.19', '113.17'], ['Malaysia', '64.73', '111.12'], ['Bulgaria', '63.96', '115.00'], ['Malta', '63.17', '109.69'], ['Morocco', '62.73', '107.91'], ['Kenya', '62.20', '108.02'], ['Colombia', '61.41', '111.85'], ['United Arab Emirates', '61.34', '106.31'], ['Sudan', '61.01', '107.64'], ['Fiji', '60.79', '105.82'], ['Kuwait', '59.63', '105.21'], ['Hong Kong', '59.50', '106.24'], ['Paraguay', '59.13', '105.75'], ['Guyana', '59.09', '104.86'], ['Georgia', '58.79', '102.90'], ['Bosnia And Herzegovina', '58.54', '101.95'], ['Brazil', '58.03', '98.78'], ['Italy', '57.75', '99.09'], ['Oman', '57.43', '99.01'], ['Moldova', '57.24', '98.51'], ['Serbia', '56.60', '98.51'], ['Argentina', '55.88', '97.37'], ['Kyrgyzstan', '55.46', '100.02'], ['Costa Rica', '55.32', '96.86'], ['Libya', '54.07', '91.14'], ['Belgium', '53.84', '91.41'], ['Namibia', '53.28', '93.79'], ['Ecuador', '53.20', '89.18'], ['Belize', '51.60', '91.00'], ['Panama', '50.91', '94.97'], ['Poland', '50.55', '86.00'], ['Romania', '50.55', '84.29'], ['Montenegro', '48.99', '85.87'], ['Puerto Rico', '48.03', '82.39'], ['Slovakia', '47.94', '82.63'], ['Syria', '47.42', '81.05'], ['Mauritius', '47.32', '85.23'], ['Spain', '46.30', '76.79'], ['Hungary', '46.25', '79.39'], ['France', '45.94', '77.19'], ['Belarus', '45.12', '77.21'], ['Greece', '44.87', '74.52'], ['Latvia', '43.43', '73.00'], ['Czech Republic', '42.87', '73.78'], ['Brunei', '40.79', '73.85'], ['Singapore', '40.40', '68.36'], ['Japan', '38.22', '63.67'], ['Netherlands', '34.97', '57.32'], ['Bahamas', '34.65', '57.89'], ['Austria', '33.96', '58.19'], ['United Kingdom', '33.95', '55.48'], ['Luxembourg', '33.50', '55.45'], ['Cyprus', '32.88', '53.01'], ['Croatia', '32.76', '53.81'], ['Portugal', '32.61', '53.88'], ['Denmark', '31.79', '49.92'], ['Uruguay', '31.72', '54.16'], ['United States', '31.45', '55.74'], ['Slovenia', '31.45', '56.66'], ['Lithuania', '29.60', '49.36'], ['Turkmenistan', '28.45', '47.59'], ['Germany', '28.32', '44.98'], ['Ireland', '27.97', '49.69'], ['Canada', '27.30', '44.58'], ['Switzerland', '24.07', '40.42'], ['Uzbekistan', '23.79', '39.66'], ['Norway', '23.70', '38.39'], ['Australia', '21.63', '33.67'], ['New Zealand', '17.61', '29.85'], ['Estonia', '15.53', '30.20'], ['Sweden', '15.14', '24.81'], ['Finland', '14.91', '26.06'], ['Iceland', '13.78', '24.49'], ['Reunion', '11.03', '34.34'], ['Bermuda', '3.24', '8.38']], 'property-investment_2014': [['Country', 'Price To Income Ratio', 'Gross Rental Yield City Centre', 'Gross Rental Yield Outside of Centre', 'Price To Rent Ratio City Centre', 'Price To Rent Ratio Outside Of City Centre', 'Mortgage As A Percentage Of Income', 'Affordability Index'], ['El Salvador', '42.41', '3.51', '1.00', '28.48', '100.00', '596.27', '0.17'], ['Georgia', '32.31', '5.32', '1.79', '18.80', '55.85', '450.31', '0.22'], ['Syria', '29.11', '3.94', '4.31', '25.40', '23.20', '317.54', '0.31'], ['Hong Kong', '27.06', '3.02', '3.17', '33.16', '31.51', '174.02', '0.57'], ['China', '26.13', '2.89', '3.22', '34.57', '31.02', '226.14', '0.44'], ['Uganda', '23.03', '2.33', '12.19', '42.97', '8.20', '297.87', '0.34'], ['Singapore', '22.59', '3.83', '4.22', '26.11', '23.70', '142.16', '0.70'], ['Nepal', '21.28', '1.97', '2.71', '50.73', '36.83', '253.71', '0.39'], ['Iran', '20.63', '5.04', '5.62', '19.86', '17.80', '440.04', '0.23'], ['Ghana', '20.41', '11.56', '13.25', '8.65', '7.54', '503.91', '0.20'], ['Venezuela', '20.19', '8.64', '7.65', '11.58', '13.07', '296.96', '0.34'], ['Armenia', '19.28', '5.61', '5.80', '17.81', '17.25', '279.29', '0.36'], ['Thailand', '19.07', '4.73', '3.85', '21.12', '26.01', '166.13', '0.60'], ['Indonesia', '18.79', '5.77', '5.20', '17.32', '19.22', '200.47', '0.50'], ['Philippines', '18.78', '3.65', '3.31', '27.42', '30.20', '220.91', '0.45'], ['Algeria', '18.61', '3.17', '4.37', '31.56', '22.89', '151.12', '0.66'], ['Ethiopia', '18.57', '12.83', '11.76', '7.79', '8.51', '237.63', '0.42'], ['Lebanon', '18.30', '3.96', '6.00', '25.23', '16.67', '155.77', '0.64'], ['Cambodia', '18.24', '9.16', '6.35', '10.92', '15.74', '214.10', '0.47'], ['Vietnam', '17.78', '5.59', '6.85', '17.90', '14.60', '237.72', '0.42'], ['Moldova', '17.73', '5.35', '5.58', '18.71', '17.92', '271.29', '0.37'], ['Morocco', '17.57', '5.47', '4.41', '18.28', '22.69', '155.11', '0.64'], ['Taiwan', '17.33', '1.59', '2.53', '63.02', '39.52', '105.33', '0.95'], ['Serbia', '16.86', '3.05', '3.33', '32.84', '30.04', '160.94', '0.62'], ['Belarus', '16.81', '4.71', '5.13', '21.24', '19.47', '556.65', '0.18'], ['Azerbaijan', '16.59', '8.74', '11.19', '11.44', '8.94', '190.52', '0.52'], ['North Macedonia', '16.18', '3.64', '3.73', '27.49', '26.81', '172.64', '0.58'], ['Montenegro', '16.03', '3.06', '3.23', '32.65', '30.95', '185.22', '0.54'], ['Ukraine', '15.95', '5.67', '6.25', '17.62', '16.00', '301.69', '0.33'], ['Brazil', '14.96', '4.44', '4.59', '22.50', '21.80', '178.83', '0.56'], ['Peru', '14.82', '4.72', '5.34', '21.20', '18.73', '172.10', '0.58'], ['Albania', '14.76', '3.78', '5.37', '26.43', '18.62', '146.24', '0.68'], ['Russia', '14.67', '7.10', '6.49', '14.09', '15.40', '211.44', '0.47'], ['Colombia', '14.23', '5.32', '5.30', '18.79', '18.87', '191.96', '0.52'], ['Pakistan', '13.92', '3.23', '3.53', '30.97', '28.31', '212.14', '0.47'], ['Nigeria', '13.86', '4.84', '5.14', '20.66', '19.45', '273.89', '0.37'], ['Trinidad And Tobago', '13.38', '8.91', '3.56', '11.22', '28.06', '138.22', '0.72'], ['Croatia', '13.37', '2.87', '3.23', '34.89', '30.99', '121.41', '0.82'], ['Romania', '13.24', '4.81', '4.83', '20.80', '20.71', '130.21', '0.77'], ['Lithuania', '12.91', '4.04', '4.06', '24.76', '24.61', '94.66', '1.06'], ['Israel', '12.83', '3.60', '3.73', '27.74', '26.82', '92.60', '1.08'], ['Latvia', '12.71', '3.84', '5.64', '26.03', '17.74', '91.93', '1.09'], ['Ecuador', '12.70', '8.54', '7.49', '11.71', '13.35', '129.67', '0.77'], ['Mauritius', '12.40', '3.98', '3.68', '25.13', '27.20', '132.73', '0.75'], ['Sri Lanka', '12.39', '6.71', '3.72', '14.91', '26.87', '197.99', '0.51'], ['Italy', '12.15', '2.83', '3.55', '35.38', '28.18', '98.44', '1.02'], ['Bosnia And Herzegovina', '11.97', '2.98', '3.25', '33.55', '30.81', '114.57', '0.87'], ['Greece', '11.74', '3.40', '3.41', '29.45', '29.37', '93.91', '1.06'], ['Uruguay', '11.60', '5.85', '6.47', '17.09', '15.46', '125.44', '0.80'], ['Poland', '11.37', '4.43', '4.79', '22.56', '20.86', '94.62', '1.06'], ['South Korea', '11.35', '3.19', '4.14', '31.31', '24.15', '86.32', '1.16'], ['Kazakhstan', '11.35', '6.87', '7.45', '14.56', '13.42', '164.92', '0.61'], ['Tunisia', '11.12', '5.34', '6.54', '18.73', '15.29', '118.19', '0.85'], ['Egypt', '11.09', '7.36', '8.22', '13.59', '12.17', '129.33', '0.77'], ['Slovenia', '11.09', '3.91', '3.98', '25.58', '25.13', '92.12', '1.09'], ['Bangladesh', '11.04', '4.26', '3.87', '23.46', '25.85', '197.32', '0.51'], ['Spain', '10.45', '3.71', '4.36', '26.97', '22.92', '73.57', '1.36'], ['Czech Republic', '10.43', '4.03', '4.56', '24.81', '21.95', '74.09', '1.35'], ['France', '10.32', '2.83', '3.91', '35.33', '25.61', '73.05', '1.37'], ['Dominican Republic', '10.30', '4.71', '9.00', '21.25', '11.12', '165.07', '0.61'], ['Estonia', '10.19', '4.77', '5.31', '20.95', '18.82', '69.39', '1.44'], ['India', '10.16', '3.34', '3.94', '29.90', '25.36', '126.43', '0.79'], ['Bulgaria', '9.87', '5.44', '5.81', '18.38', '17.22', '101.23', '0.99'], ['Panama', '9.73', '10.95', '8.24', '9.13', '12.14', '83.19', '1.20'], ['Hungary', '9.63', '3.91', '4.25', '25.57', '23.51', '101.62', '0.98'], ['Slovakia', '9.51', '6.23', '6.02', '16.05', '16.62', '73.29', '1.36'], ['Chile', '9.45', '5.08', '4.56', '19.69', '21.95', '76.29', '1.31'], ['Sweden', '9.41', '2.60', '3.33', '38.46', '29.99', '65.03', '1.54'], ['Kenya', '9.33', '14.51', '7.86', '6.89', '12.73', '159.98', '0.63'], ['Zimbabwe', '9.26', '9.42', '10.08', '10.62', '9.92', '246.67', '0.41'], ['Austria', '9.17', '3.49', '3.81', '28.69', '26.26', '63.91', '1.56'], ['Malta', '9.10', '2.53', '4.42', '39.55', '22.61', '63.89', '1.57'], ['Honduras', '9.00', '5.59', '7.14', '17.90', '14.01', '124.13', '0.81'], ['Iraq', '8.98', '8.78', '8.90', '11.39', '11.23', '113.67', '0.88'], ['Argentina', '8.95', '4.62', '4.77', '21.65', '20.98', '186.31', '0.54'], ['Bolivia', '8.58', '7.28', '6.90', '13.73', '14.48', '85.57', '1.17'], ['Portugal', '8.41', '5.84', '6.49', '17.13', '15.40', '62.51', '1.60'], ['Japan', '8.34', '4.06', '3.28', '24.64', '30.47', '50.36', '1.99'], ['Malaysia', '8.04', '5.01', '4.68', '19.97', '21.37', '63.97', '1.56'], ['Guatemala', '8.04', '8.05', '9.19', '12.43', '10.88', '93.07', '1.07'], ['Jordan', '7.95', '7.39', '7.18', '13.53', '13.93', '81.47', '1.23'], ['Finland', '7.83', '3.61', '4.40', '27.68', '22.72', '49.20', '2.03'], ['Luxembourg', '7.75', '4.84', '4.70', '20.66', '21.25', '48.42', '2.07'], ['United Kingdom', '7.74', '4.70', '5.16', '21.26', '19.39', '57.65', '1.73'], ['Australia', '7.44', '5.15', '5.46', '19.42', '18.30', '64.46', '1.55'], ['Norway', '7.42', '4.62', '4.99', '21.66', '20.03', '52.74', '1.90'], ['Iceland', '7.15', '7.72', '7.22', '12.96', '13.86', '69.60', '1.44'], ['Cyprus', '7.07', '4.96', '4.70', '20.17', '21.27', '62.70', '1.59'], ['Switzerland', '7.05', '3.61', '3.60', '27.69', '27.78', '42.72', '2.34'], ['Bahrain', '6.92', '10.70', '8.82', '9.34', '11.34', '69.50', '1.44'], ['Costa Rica', '6.88', '8.78', '8.63', '11.38', '11.59', '95.39', '1.05'], ['Turkey', '6.86', '5.81', '6.93', '17.20', '14.43', '90.40', '1.11'], ['Kuwait', '6.78', '6.72', '5.43', '14.89', '18.42', '54.93', '1.82'], ['Mozambique', '6.59', '17.55', '14.82', '5.70', '6.75', '140.56', '0.71'], ['Mexico', '6.47', '6.36', '5.32', '15.72', '18.80', '80.58', '1.24'], ['Denmark', '6.37', '4.50', '4.73', '22.20', '21.13', '44.50', '2.25'], ['Netherlands', '6.08', '5.72', '5.83', '17.48', '17.16', '46.27', '2.16'], ['Belgium', '5.98', '5.49', '6.09', '18.21', '16.43', '43.19', '2.32'], ['Ireland', '5.74', '5.87', '5.69', '17.05', '17.58', '43.33', '2.31'], ['Qatar', '5.72', '9.71', '6.49', '10.30', '15.40', '45.36', '2.20'], ['Germany', '5.60', '4.51', '4.78', '22.17', '20.91', '37.98', '2.63'], ['Canada', '5.57', '5.54', '6.06', '18.05', '16.51', '38.70', '2.58'], ['Bahamas', '5.47', '5.55', '7.52', '18.03', '13.30', '60.48', '1.65'], ['New Zealand', '5.30', '6.77', '7.89', '14.78', '12.67', '44.44', '2.25'], ['United Arab Emirates', '5.26', '8.75', '10.38', '11.43', '9.63', '45.48', '2.20'], ['Puerto Rico', '5.10', '5.20', '6.80', '19.24', '14.70', '41.82', '2.39'], ['Libya', '4.83', '17.43', '13.52', '5.74', '7.40', '47.01', '2.13'], ['Angola', '4.54', '33.49', '17.58', '2.99', '5.69', '71.69', '1.39'], ['Jamaica', '3.87', '9.15', '15.66', '10.93', '6.39', '55.16', '1.81'], ['South Africa', '3.45', '9.13', '9.03', '10.95', '11.08', '36.95', '2.71'], ['Saudi Arabia', '3.25', '6.63', '6.24', '15.08', '16.01', '24.29', '4.12'], ['Namibia', '3.22', '26.12', '30.07', '3.83', '3.33', '37.49', '2.67'], ['Oman', '2.95', '11.18', '12.46', '8.94', '8.02', '26.71', '3.74'], ['United States', '2.43', '11.01', '12.58', '9.08', '7.95', '17.99', '5.56'], ['Tanzania', '2.04', '59.59', '27.83', '1.68', '3.59', '34.95', '2.86']], 'quality-of-life_2011': [['Country', 'Quality of Life Index', 'Purchasing Power Index', 'Safety Index', 'Health Care Index', 'Cost of Living Index', 'Property Price to Income Ratio', 'Traffic Commute Time Index', 'Pollution Index', 'Climate Index']], 'traffic_2010': [['Country', 'Traffic Index', 'Time Index(in minutes)', 'Time Exp. Index', 'Inefficiency Index', 'CO2 Emission Index']], 'traffic_2015': [['Country', 'Traffic Index', 'Time Index(in minutes)', 'Time Exp. Index', 'Inefficiency Index', 'CO2 Emission Index'], ['Kenya', '317.24', '65.20', '23012.87', '253.96', '7123.60'], ['Egypt', '293.39', '56.85', '12243.24', '298.66', '11796.20'], ['Bangladesh', '280.43', '58.00', '13477.89', '330.05', '7772.86'], ['Bolivia', '243.93', '55.00', '10411.95', '254.22', '5033.33'], ['Nigeria', '241.71', '58.67', '14228.36', '240.38', '2328.67'], ['Jordan', '232.05', '51.40', '7368.18', '224.09', '6374.20'], ['Iran', '214.14', '47.44', '4753.91', '202.60', '6974.74'], ['South Africa', '208.39', '42.98', '2618.22', '202.37', '10002.42'], ['Philippines', '202.31', '45.50', '3724.39', '217.82', '6565.46'], ['Thailand', '200.79', '42.36', '2382.55', '239.58', '8862.14'], ['Brazil', '199.40', '46.34', '4149.46', '246.50', '5321.17'], ['Russia', '198.51', '47.08', '4551.20', '197.85', '4885.94'], ['India', '195.53', '45.24', '3597.83', '207.68', '5760.83'], ['Japan', '194.55', '51.05', '7103.79', '203.98', '2019.09'], ['Ecuador', '194.39', '45.67', '3806.43', '133.25', '5698.33'], ['Turkey', '194.22', '46.32', '4138.81', '198.73', '4825.94'], ['Indonesia', '186.26', '41.63', '2124.33', '248.99', '6849.71'], ['Malaysia', '181.23', '39.40', '1447.11', '209.35', '7978.29'], ['Argentina', '175.34', '41.39', '2043.50', '164.21', '5765.56'], ['Israel', '175.23', '41.25', '1997.57', '174.67', '5787.00'], ['Hong Kong', '171.92', '46.25', '4102.60', '182.29', '2315.62'], ['Singapore', '170.76', '44.07', '3065.05', '129.13', '3595.87'], ['Colombia', '162.94', '44.55', '3276.21', '173.10', '2304.09'], ['Canada', '161.56', '38.88', '1312.67', '198.88', '5233.99'], ['Mexico', '158.59', '36.89', '874.65', '184.19', '6169.37'], ['United States', '158.47', '35.96', '706.31', '179.28', '6813.52'], ['Ukraine', '157.51', '40.04', '1626.27', '180.43', '4058.61'], ['China', '150.98', '37.48', '992.08', '156.95', '4826.16'], ['Cambodia', '150.01', '33.33', '351.79', '134.37', '7453.33'], ['Chile', '149.19', '40.83', '1863.79', '111.93', '2982.17'], ['Lebanon', '148.72', '32.43', '265.43', '137.82', '7790.00'], ['Uruguay', '147.57', '45.00', '3485.06', '157.64', '960.00'], ['Kazakhstan', '146.90', '41.80', '2183.39', '64.56', '2534.40'], ['Mongolia', '143.70', '36.86', '867.44', '100.07', '4541.43'], ['Australia', '142.46', '36.25', '756.24', '153.00', '4400.63'], ['Italy', '142.07', '35.91', '698.30', '152.91', '4538.88'], ['Vietnam', '141.69', '36.40', '782.79', '123.14', '4384.80'], ['Netherlands', '140.43', '35.45', '624.88', '280.21', '4000.00'], ['Venezuela', '139.90', '30.60', '138.69', '126.56', '7443.00'], ['Puerto Rico', '139.58', '32.00', '230.25', '106.47', '6738.67'], ['Qatar', '132.56', '29.27', '81.09', '97.78', '7121.82'], ['Panama', '130.46', '28.12', '50.26', '106.09', '7216.25'], ['Georgia', '128.99', '38.00', '1104.63', '121.88', '2182.00'], ['Greece', '128.78', '33.18', '335.69', '139.97', '4284.16'], ['United Arab Emirates', '128.27', '29.90', '105.29', '155.15', '5722.57'], ['United Kingdom', '127.76', '34.00', '426.55', '177.57', '3573.45'], ['Dominican Republic', '127.02', '27.50', '39.57', '59.28', '7315.00'], ['Sri Lanka', '126.82', '30.83', '151.61', '99.43', '5431.67'], ['North Macedonia', '122.58', '33.17', '334.60', '202.42', '3236.33'], ['Kuwait', '119.48', '25.00', '25.00', '114.44', '6206.67'], ['Poland', '118.16', '34.67', '511.73', '101.65', '2579.75'], ['Bahrain', '116.25', '27.00', '33.58', '95.83', '5426.40'], ['Saudi Arabia', '113.05', '26.14', '27.58', '103.92', '5107.29'], ['Belarus', '113.05', '30.57', '137.17', '82.47', '3805.14'], ['Pakistan', '112.61', '25.14', '25.15', '82.38', '5383.57'], ['Bulgaria', '109.48', '33.43', '362.54', '138.47', '2046.70'], ['Romania', '108.25', '30.69', '143.43', '113.72', '3016.61'], ['Ireland', '108.08', '32.60', '280.17', '133.01', '2229.23'], ['Moldova', '106.98', '24.60', '24.60', '83.01', '4666.00'], ['Spain', '106.47', '28.91', '69.65', '136.57', '3309.73'], ['Taiwan', '106.28', '28.25', '52.88', '97.09', '3709.00'], ['Lithuania', '105.38', '31.33', '182.36', '138.01', '2380.56'], ['Belgium', '102.46', '26.69', '30.89', '129.52', '3460.44'], ['Croatia', '102.35', '30.50', '133.42', '109.94', '2481.27'], ['Finland', '100.39', '33.17', '334.60', '106.76', '1489.89'], ['Serbia', '99.85', '27.79', '44.02', '111.82', '3008.97'], ['Portugal', '99.79', '28.20', '51.71', '93.14', '2997.85'], ['Germany', '98.41', '31.08', '166.45', '113.71', '1914.97'], ['Slovakia', '98.37', '30.40', '128.32', '121.32', '2082.00'], ['South Korea', '96.62', '31.33', '182.36', '73.77', '1865.33'], ['Denmark', '94.37', '27.85', '45.02', '110.91', '2428.46'], ['Hungary', '92.87', '30.12', '114.63', '99.11', '1771.46'], ['New Zealand', '92.36', '28.10', '49.66', '67.84', '2399.14'], ['Czech Republic', '91.65', '31.47', '191.30', '62.66', '1477.27'], ['Latvia', '90.11', '24.00', '24.00', '52.28', '2913.60'], ['Armenia', '88.83', '26.09', '27.36', '57.84', '2490.55'], ['Syria', '86.67', '20.88', '20.88', '64.00', '2832.00'], ['France', '85.70', '28.60', '61.12', '69.52', '1676.47'], ['Sweden', '84.03', '26.90', '32.67', '92.48', '1747.05'], ['Greenland', '82.47', '18.00', '18.00', '74.92', '2660.00'], ['Switzerland', '80.46', '25.63', '25.91', '65.53', '1734.00'], ['Norway', '74.58', '25.30', '25.34', '48.17', '1391.40'], ['Slovenia', '74.57', '18.82', '18.82', '31.97', '2094.36'], ['Cyprus', '73.72', '19.00', '19.00', '34.31', '1980.22'], ['Estonia', '69.25', '22.44', '22.44', '23.51', '1385.56'], ['Bosnia And Herzegovina', '67.19', '21.90', '21.90', '36.13', '1197.00'], ['Austria', '66.87', '25.86', '26.51', '44.46', '852.14'], ['Turkmenistan', '45.49', '11.75', '11.75', '10.22', '735.00']], 'traffic_2019': [['Country', 'Traffic Index', 'Time Index(in minutes)', 'Time Exp. Index', 'Inefficiency Index', 'CO2 Emission Index'], ['Egypt', '236.87', '49.17', '5807.05', '291.84', '8913.49'], ['Sri Lanka', '233.57', '51.90', '7753.05', '281.56', '5903.18'], ['Iran', '221.53', '48.38', '5306.47', '231.32', '7241.90'], ['India', '201.14', '45.71', '3828.27', '235.01', '6119.38'], ['Jordan', '199.12', '42.43', '2408.89', '222.13', '8594.71'], ['South Africa', '196.65', '40.33', '1709.46', '247.37', '9850.16'], ['Philippines', '196.62', '44.15', '3099.88', '243.43', '6591.69'], ['Turkey', '195.50', '44.77', '3378.12', '215.11', '6075.73'], ['Indonesia', '193.19', '42.93', '2598.10', '249.49', '6971.18'], ['Russia', '188.73', '46.00', '3975.77', '192.17', '4331.50'], ['Brazil', '186.41', '43.37', '2772.67', '207.77', '5772.19'], ['Colombia', '182.80', '45.06', '3511.20', '197.03', '4153.80'], ['Thailand', '178.43', '39.40', '1447.44', '226.43', '7385.83'], ['United Arab Emirates', '176.95', '37.46', '987.59', '259.31', '8457.10'], ['Lebanon', '176.09', '37.36', '966.30', '200.86', '8737.07'], ['Argentina', '175.61', '43.04', '2642.39', '190.99', '4535.53'], ['Mexico', '175.22', '39.08', '1365.36', '208.75', '7180.92'], ['Panama', '166.66', '36.48', '796.29', '182.13', '7826.65'], ['China', '165.27', '42.46', '2419.16', '169.12', '3675.44'], ['Pakistan', '163.23', '38.63', '1251.56', '185.54', '5715.47'], ['Kuwait', '161.48', '34.82', '532.44', '183.91', '8104.67'], ['Malaysia', '159.40', '35.25', '594.48', '175.03', '7488.77'], ['Singapore', '154.36', '42.15', '2306.35', '165.18', '2635.37'], ['Israel', '150.55', '36.32', '768.08', '164.69', '5430.17'], ['United States', '149.66', '32.87', '305.42', '199.84', '7254.78'], ['Qatar', '147.86', '31.71', '208.30', '155.43', '7965.31'], ['Australia', '146.93', '35.29', '600.16', '174.22', '5467.89'], ['South Korea', '145.57', '40.02', '1618.91', '153.22', '2802.76'], ['Ukraine', '140.70', '37.36', '967.02', '125.35', '3727.01'], ['Canada', '140.03', '33.77', '399.42', '175.39', '5334.00'], ['Ireland', '139.08', '35.85', '687.61', '166.27', '4111.63'], ['Hong Kong', '137.47', '41.00', '1916.59', '145.78', '1650.02'], ['Belgium', '136.15', '34.86', '537.96', '160.68', '4279.41'], ['Chile', '136.00', '36.79', '854.71', '120.66', '3479.48'], ['Italy', '135.37', '34.69', '514.52', '156.98', '4286.32'], ['Saudi Arabia', '135.35', '29.61', '93.13', '157.42', '6979.84'], ['Japan', '134.54', '40.03', '1622.13', '141.63', '1792.28'], ['United Kingdom', '133.25', '34.62', '505.32', '161.45', '4025.59'], ['New Zealand', '129.21', '31.19', '172.87', '161.61', '5207.49'], ['France', '128.21', '35.27', '596.62', '129.13', '3266.30'], ['Romania', '126.84', '34.36', '470.73', '128.03', '3537.39'], ['Greece', '124.32', '32.20', '245.90', '139.33', '4177.56'], ['Hungary', '123.85', '35.17', '581.80', '130.57', '2823.40'], ['Latvia', '120.01', '31.45', '189.92', '124.73', '4046.96'], ['Georgia', '116.99', '34.34', '468.79', '142.40', '2407.37'], ['Oman', '115.93', '21.51', '21.51', '246.50', '5487.20'], ['Taiwan', '112.45', '30.90', '155.20', '135.76', '3299.82'], ['Poland', '112.30', '32.15', '242.26', '102.03', '2968.09'], ['Portugal', '109.89', '29.02', '72.77', '117.93', '3780.29'], ['Belarus', '109.79', '28.78', '65.85', '92.89', '4002.28'], ['Kazakhstan', '109.17', '29.75', '98.84', '88.30', '3609.22'], ['Spain', '108.12', '29.42', '86.18', '123.49', '3399.99'], ['Netherlands', '107.40', '29.87', '103.74', '176.67', '2921.87'], ['Croatia', '105.79', '29.11', '75.74', '104.24', '3337.56'], ['Vietnam', '105.18', '28.33', '54.72', '109.43', '3479.98'], ['Slovakia', '104.58', '29.58', '92.17', '191.57', '2658.30'], ['Serbia', '103.55', '29.74', '98.42', '113.47', '2834.61'], ['Sweden', '101.79', '30.29', '123.00', '131.76', '2394.14'], ['Lithuania', '99.60', '27.15', '35.17', '93.13', '3234.62'], ['Bulgaria', '98.58', '28.79', '66.14', '88.72', '2729.49'], ['Germany', '98.09', '29.91', '105.71', '114.59', '2226.46'], ['Slovenia', '97.65', '24.81', '24.81', '132.00', '3177.34'], ['North Macedonia', '96.09', '27.94', '46.62', '102.06', '2623.36'], ['Czech Republic', '94.93', '30.02', '110.22', '75.95', '2088.68'], ['Norway', '94.54', '27.12', '34.86', '115.65', '2576.96'], ['Finland', '94.01', '30.41', '128.60', '83.28', '1860.60'], ['Iceland', '92.95', '19.74', '19.74', '74.23', '3618.09'], ['Bosnia And Herzegovina', '92.76', '26.43', '29.05', '69.82', '2765.78'], ['Switzerland', '90.28', '29.05', '73.90', '98.73', '1822.80'], ['Cyprus', '90.08', '20.27', '20.27', '60.39', '3310.09'], ['Denmark', '87.10', '28.51', '58.95', '110.57', '1631.47'], ['Estonia', '83.54', '25.75', '26.20', '117.32', '1751.07'], ['Austria', '78.08', '25.15', '25.16', '73.47', '1547.64']]})


class WelfareType(enum.Enum):
    cost_of_living = 'cost-of-living'
    crime = 'crime'
    health_care = 'health-care'
    pollution = 'pollution'
    property_investment = 'property-investment'
    quality_of_life = 'quality-of-life'
    traffic = 'traffic'


LOGGER_NAME = 'welfare_logger'
logger = logging.getLogger(LOGGER_NAME)

FIRST_YEAR = 2012

# Logger
LOG_FILE_NAME = 'welfare_log_file.log'

# URL Requests/Responses
SUBJECT = '<SUBJECT>'
YEAR = '<YEAR>'
MAIN_URL = f'https://www.numbeo.com/{SUBJECT}/rankings_by_country.jsp?title={YEAR}'
HTTP_SUCCESS = 200
CURRENT_YEAR = int(datetime.datetime.now().year)

# Command Line Interface
TABLE_HELP_DESC = f'''Run this command to receive only one table with the following 2 arguments:
                   \nsubject: {WelfareType.cost_of_living,
                               WelfareType.crime,
                               WelfareType.health_care,
                               WelfareType.pollution,
                               WelfareType.property_investment,
                               WelfareType.quality_of_life,
                               WelfareType.traffic}
                    \nyear: ranges from {FIRST_YEAR} to last year 
                    Please run the command in the following manner:
                    <subject1> <year1> <subject2> <year2> <subject3> <year3>...<subjectN> <yearN>'''
ALL_TABLES_HELP_DESC = '''Run this command to receive all of the tables'''
HELP_DESC = 'You have 2 available commands: --table and --all_tables'
INVALID_PARAMS = 'You have entered invalid parameters\n' + HELP_DESC

# MySQL
DATABASE_NAME = 'welfare'
HOST = 'localhost'
USERNAME = 'root'
PASSWORD = 'Yc7350328'


def exit_program():
    sys.exit()


def setup():
    setup_logger()


def setup_logger():
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    formatter = logging.Formatter(
        '[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        '%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)  # write to the file LOG_FILE_NAME
    logger.addHandler(logging.StreamHandler(sys.stdout))  # adds print to console
    logger.level = logging.INFO
