import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            temperature INT NOT NULL,
            humidity INT NOT NULL,
            description VARCHAR(255) NOT NULL,
            data_noted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
    """)

    conn.commit()
    conn.close()

def fetch_dataframe(days: int = 7) -> pd.DataFrame:

    query = """
        SELECT city_name, temperature, humidity, description, data_noted_at
        FROM weather_data
        WHERE data_noted_at >= NOW() - INTERVAL %s DAY
        ORDER BY data_noted_at ASC
    """

    df = pd.read_sql_query(query, engine, params=(days,))
    
    df = df.dropna(subset=["city_name", "temperature", "humidity", "data_noted_at"])
    df = df[(df["temperature"] > -100) & (df["temperature"] < 80)]
    df = df[(df["humidity"] >= 0) & (df["humidity"] <= 100)]
    df["data_noted_at"] = pd.to_datetime(df["data_noted_at"], utc=True)
    df["data_noted_at"] = df["data_noted_at"].dt.tz_convert("Asia/Kolkata")

    today_str = datetime.today().strftime("%Y-%m-%d")
    
    df.to_parquet(f"{today_str}.parquet", engine="pyarrow", index=False)
    return df

def past_week_averages(df: pd.DataFrame):
    return df.groupby("city_name")[["temperature", "humidity"]].mean().round(2)

def week_highs(df: pd.DataFrame):
    temp_high = df.loc[df["temperature"].idxmax()][["city_name", "temperature", "data_noted_at"]]
    hum_high = df.loc[df["humidity"].idxmax()][["city_name", "humidity", "data_noted_at"]]
    return temp_high, hum_high

def most_common_condition(df: pd.DataFrame):
    if df.empty:
        return None
    return df["description"].value_counts().idxmax(), df["description"].value_counts().max()


def plot_matplotlib(df: pd.DataFrame):
    if df.empty:
        print("No data available for plotting.")
        return
    
    cities = df["city_name"].unique()
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 1, 1)
    for city in cities:
        city_data = df[df["city_name"] == city]
        plt.plot(city_data["data_noted_at"], city_data["temperature"], marker="o", label=city)
    plt.title("Temperature Over Past 7 Days")
    plt.xlabel("Date/Time")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    for city in cities:
        city_data = df[df["city_name"] == city]
        plt.plot(city_data["data_noted_at"], city_data["humidity"], marker="x", label=city)
    plt.title("Humidity Over Past 7 Days")
    plt.xlabel("Date/Time")
    plt.ylabel("Humidity (%)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    today_str = datetime.today().strftime("%Y-%m-%d")
    filename = f"weather_report_{today_str}.png"
    plt.savefig(filename, dpi=300)
    print(f"Matplotlib report saved as {filename}")

def plot_plotly(df: pd.DataFrame):
    if df.empty:
        print("No data available for interactive plots.")
        return
    
    today_str = datetime.today().strftime("%Y-%m-%d")

    fig_temp = px.line(
        df, x="data_noted_at", y="temperature", color="city_name",
        title="Temperature Over Past 7 Days"
    )
    fig_temp.update_layout(
        xaxis_title="Date/Time", yaxis_title="Temperature (°C)",
        legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center", yanchor="bottom")
    )
    fig_temp.write_html(f"temperature_report_{today_str}.html")

    fig_hum = px.line(
        df, x="data_noted_at", y="humidity", color="city_name",
        title="Humidity Over Past 7 Days"
    )
    fig_hum.update_layout(
        xaxis_title="Date/Time", yaxis_title="Humidity (%)",
        legend=dict(orientation="h", y=-0.3, x=0.5, xanchor="center", yanchor="bottom")
    )
    fig_hum.write_html(f"humidity_report_{today_str}.html")

    print(f"Plotly reports saved as temperature_report_{today_str}.html and humidity_report_{today_str}.html")


def report():
    init_db()
    df = fetch_dataframe()

    print("\n=== Weather Report (Past 7 Days) ===")

    print("\n--- Average Conditions by City ---")
    print(past_week_averages(df))

    print("\n--- Weekly Highs ---")
    if not df.empty:
        temp_high, hum_high = week_highs(df)
        print(f"Highest Temperature: {temp_high['temperature']}°C in {temp_high['city_name']} at {temp_high['data_noted_at']}")
        print(f"Highest Humidity: {hum_high['humidity']}% in {hum_high['city_name']} at {hum_high['data_noted_at']}")

    print("\n--- Most Common Condition ---")
    common = most_common_condition(df)
    if common:
        print(f"{common[0]} ({common[1]} times)")
    else:
        print("No data available.")

    plot_matplotlib(df)
    plot_plotly(df)


if __name__ == "__main__":
    report()
