import requests
import sys
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def init_db():
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    city_name VARCHAR(100) NOT NULL,
                    temperature INT NOT NULL,
                    humidity INT NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    data_noted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)
    except Error as e:
        print(f"error, {e}")
    finally:
        if conn.is_connected():
            conn.commit()
            conn.close()


def insert_weather_data(city_name, temperature, humidity, description):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO weather_data (city_name, temperature, humidity, description)
            VALUES (%s, %s, %s, %s)
        """, (city_name, temperature, humidity, description))
        conn.commit()
        
    except Error as e:
        print(f"error,{e}")
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def fetch_weather(city_name: str):
    if not API_KEY:
        raise ValueError("API key not found. Please set OPENWEATHER_API_KEY as an environment variable.")
    
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    
    data = response.json()
    
    city = data["name"]
    temperature = round(data["main"]["temp"])
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    
    insert_weather_data(city, temperature, humidity, description)
    
    return {
        "city": city,
        "temperature (°C)": temperature,
        "humidity (%)": humidity,
        "description": description
    }


if __name__ == "__main__":
    init_db()
    
    if len(sys.argv) > 1:
        init_db()
        city = " ".join(sys.argv[1:])
        fetch_weather(city)
        sys.exit(0)

    cities = [
        "New York",
        "São Paulo",
        "London",
        "Cairo",
        "Mumbai",
        "Tokyo",
        "Sydney"
    ]
    
    for city in cities:
        weather = fetch_weather(city)