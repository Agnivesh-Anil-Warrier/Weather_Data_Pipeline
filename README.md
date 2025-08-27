# 🌦️ Weather Data Pipeline

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/Agnivesh-Anil-Warrier/weather_data_pipeline)](https://github.com/Agnivesh-Anil-Warrier/weather_data_pipeline/issues)
[![Last Commit](https://img.shields.io/github/last-commit/Agnivesh-Anil-Warrier/weather_data_pipeline)](https://github.com/Agnivesh-Anil-Warrier/weather_data_pipeline)

An end-to-end weather data pipeline that:
- Fetches live weather data from the **OpenWeather API**
- Stores it in a **MySQL database**
- Processes & validates data with **Pandas**
- Generates both **static (Matplotlib)** and **interactive (Plotly)** reports
- Exports **Parquet** files for analysis

---

## ✨ Features
- 🌍 Fetch live weather for multiple global cities  
- 🗄️ Store historical weather data in MySQL  
- 🧹 Data validation (temperature, humidity ranges, etc.)  
- 📊 Daily parquet exports for analysis pipelines  
- 🖼️ Automated visual reports:  
  - Static PNGs (Matplotlib)  
  - Interactive HTML dashboards (Plotly)  
- 🔐 Secure configuration with `.env` (API key & DB credentials)  

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/Agnivesh-Anil-Warrier/weather_data_pipeline.git
cd weather_data_pipeline

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables in .env
OPENWEATHER_API_KEY=your_api_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=weather
```

## Usage

To fetch and insert live weather data:
  ```bash
  python weather_fetcher.py
  ```
To generate weekly reports:
  ```bash
  python weather_report.py
  ```
Matplotlib reports → saved as .png and Plotly reports → saved as interactive .html

---
## Project Structure
  ```bash
    weather_data_pipeline/
    │── weather_fetcher.py   # Fetch weather data & store in DB
    │── weather_report.py    # Generate reports from historical data
    │── requirements.txt     # Project dependencies
    │── .env.example         # Example env file (copy → .env)
    │── LICENSE              # License (MIT)
    │── README.md            # Documentation
  ```

## ⭐ Acknowledgments  

- [OpenWeather API](https://openweathermap.org/api) – for providing weather data  
- [Pandas](https://pandas.pydata.org/) – for data handling  
- [Matplotlib](https://matplotlib.org/) – for visualization  
- [Plotly](https://plotly.com/python/) – for interactive visualization  
