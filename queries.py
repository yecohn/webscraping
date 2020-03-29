import sqlite3
import pandas as pd
DATABASE_NAME= 'parser.db'


with sqlite3.connect(DATABASE_NAME) as con:
    cur = con.cursor()
    df = pd.read_sql_query('SELECT * from crime LIMIT 100', con)

    print(df)