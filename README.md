# 🌦️ Weather ETL Pipeline

**A Python-based ETL pipeline for collecting, transforming, and storing current weather data using the OpenWeatherMap API and SQLite.**

> Developed by a 15-year-old Python and Data Engineering enthusiast.

---

# 🇬🇧 English

## 📌 Project Overview

Weather ETL Pipeline is an educational project that implements the fundamental principles of ETL (Extract, Transform, Load).

The pipeline retrieves current weather data from the OpenWeatherMap API, validates and transforms the received JSON response, and stores the processed data in an SQLite database.

The project demonstrates practical implementation of ETL architecture, working with external REST APIs, data validation, error handling, and database operations.

## ⚙️ ETL Architecture

The project consists of three main stages:

### 1. Extract — `ExtractWeather`

- Retrieves current weather data through the OpenWeatherMap REST API.
- Uses geographic coordinates to identify the requested location.
- Loads the API key from environment variables.
- Implements automatic retries using Tenacity.
- Validates API key availability and geographic coordinates.

### 2. Transform — `TransformWeather`

- Extracts the required fields from the JSON response.
- Converts values to appropriate Python data types.
- Validates temperature, atmospheric pressure, humidity, and cloudiness.
- Converts Unix timestamps into UTC datetime objects.
- Handles missing and invalid values.

### 3. Load — `LoadWeather`

- Creates an SQLite database table if it does not exist.
- Inserts processed weather records.
- Prevents duplicate records using a UNIQUE constraint on latitude, longitude, and observation time.
- Logs the number of stored records.

## 🛠️ Technologies Used

| Technology | Purpose |
|:---|:---|
| Python | Main programming language |
| SQLite3 | Relational database and data storage |
| Requests | HTTP requests to the REST API |
| Tenacity | Automatic request retries |
| Python-dotenv | Environment variable management |
| Logging | Execution and error logging |
| Dataclasses | Data class implementation |
| JSON | API response processing |

## 📁 Project Structure

```text
weather-etl-pipeline/
│
├── db_weather_info/
│   └── SQLite database (generated locally)
│
├── ETL_WEATHER_PIPELINE.py   # Main ETL pipeline
│
├── .env                      # API credentials (not committed)
├── .gitignore                # Files excluded from Git
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
