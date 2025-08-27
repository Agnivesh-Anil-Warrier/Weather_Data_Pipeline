import sqlite3
import os
import mysql.connector

sqlite_conn = sqlite3.connect("weather.db")
sqlite_cursor = sqlite_conn.cursor()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

mysql_conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
mysql_cursor = mysql_conn.cursor()

sqlite_cursor.execute("SELECT city_name, temperature, humidity, description, data_noted_at FROM weather_data")
rows = sqlite_cursor.fetchall()

insert_query = """
INSERT INTO weather_data (city_name, temperature, humidity, description, data_noted_at)
VALUES (%s, %s, %s, %s, %s)
"""

for row in rows:
    mysql_cursor.execute(insert_query, row)

mysql_conn.commit()

print(f"Migrated {len(rows)} rows successfully!")

sqlite_conn.close()
mysql_conn.close()
