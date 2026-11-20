# weather_openweather_etl
A Python-based ETL pipeline for collecting, transforming, validating, and storing weather data using OpenWeatherMap API and SQLite.

🌦️ Weather ETL Pipeline

A Python-based ETL pipeline for collecting, transforming, and storing current weather data using the OpenWeatherMap API and SQLite.

Developed by a 15-year-old Python and Data Engineering enthusiast.
🇬🇧 English
Project Overview

Weather ETL Pipeline is an educational project that implements the fundamental principles of ETL (Extract, Transform, Load).

The pipeline retrieves current weather data from the OpenWeatherMap API, validates and transforms the received JSON response, and stores the processed data in an SQLite database.

The project demonstrates practical implementation of ETL architecture, working with external REST APIs, data validation, error handling, and database operations.

ETL Architecture

The project consists of three main stages:

1. Extract — ExtractWeather
Retrieves current weather data through the OpenWeatherMap REST API.
Uses geographic coordinates to identify the requested location.
Loads the API key from environment variables.
Implements automatic retries using Tenacity.
Validates API key availability and geographic coordinates.
2. Transform — TransformWeather
Extracts the required fields from the JSON response.
Converts values to appropriate Python data types.
Validates temperature, atmospheric pressure, humidity, and cloudiness.
Converts Unix timestamps into UTC datetime objects.
Handles missing and invalid values.
3. Load — LoadWeather
Creates an SQLite database table if it does not exist.
Inserts processed weather records.
Prevents duplicate records using a UNIQUE constraint on latitude, longitude, and observation time.
Logs the number of stored records.
Technologies Used
Technology	Purpose
Python	Main programming language
SQLite3	Relational database and data storage
Requests	HTTP requests to the REST API
Tenacity	Automatic request retries
Python-dotenv	Environment variable management
Logging	Execution and error logging
Dataclasses	Data class implementation
JSON	API response processing
Project Structure
text
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

Installation and Setup
1. Clone the repository
bash
git clone https://github.com/USERNAME/weather-etl-pipeline.git

cd weather-etl-pipeline

2. Create a virtual environment
bash
python -m venv venv


Activate the virtual environment:

Windows:

bash
venv\Scripts\activate


Linux / macOS:

bash
source venv/bin/activate

3. Install dependencies
bash
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root directory:

env
API_KEY=your_openweathermap_api_key


Replace your_openweathermap_api_key with your actual OpenWeatherMap API key.

5. Run the pipeline

Run with default coordinates:

bash
python ETL_WEATHER_PIPELINE.py


Run with custom geographic coordinates and language:

bash
python ETL_WEATHER_PIPELINE.py 40.7128 -74.0060 ru


The default coordinates correspond to New York City.

Database

Processed weather data is stored in an SQLite database.

The weather table contains the following fields:

Column	Description
ID	Unique record identifier
LAT	Latitude
LON	Longitude
DESCRIPTION	Weather description
TEMP	Temperature (°C)
FEELS_LIKE	Feels-like temperature (°C)
PRESSURE	Atmospheric pressure (hPa)
HUMIDITY	Relative humidity (%)
CLOUDS	Cloudiness (%)
TIME	Observation timestamp (UTC)
COUNTRY	Country code
Data Source

Weather data is provided by the OpenWeatherMap API.

🇷🇺 Weather ETL Pipeline
Описание проекта

Weather ETL Pipeline — учебный проект, реализующий основные принципы ETL (Extract, Transform, Load).

Пайплайн получает текущие погодные данные через OpenWeatherMap API, проверяет и преобразует полученный JSON-ответ, после чего сохраняет обработанные данные в базу данных SQLite.

Проект демонстрирует практическое применение ETL-архитектуры, работу с внешними REST API, проверку качества данных, обработку ошибок и взаимодействие с базами данных.

Архитектура ETL

Проект состоит из трёх основных этапов:

1. Extract — ExtractWeather (извлечение)
Получение текущих погодных данных через OpenWeatherMap REST API.
Использование географических координат для определения местоположения.
Получение API-ключа из переменных окружения.
Автоматические повторные запросы при возникновении ошибок с использованием Tenacity.
Проверка наличия API-ключа и корректности географических координат.
2. Transform — TransformWeather (преобразование)
Извлечение необходимых полей из JSON-ответа.
Преобразование значений в соответствующие типы данных Python.
Проверка температуры, атмосферного давления, влажности и облачности.
Преобразование Unix timestamp в объекты datetime с часовым поясом UTC.
Обработка отсутствующих и некорректных значений.
3. Load — LoadWeather (загрузка)
Создание таблицы SQLite, если она ещё не существует.
Загрузка обработанных погодных данных.
Предотвращение дублирования записей с помощью ограничения UNIQUE по широте, долготе и времени наблюдения.
Логирование количества сохранённых записей.
Используемые технологии
Технология	Назначение
Python	Основной язык программирования
SQLite3	Реляционная база данных и хранение информации
Requests	HTTP-запросы к REST API
Tenacity	Автоматические повторные запросы
Python-dotenv	Работа с переменными окружения
Logging	Логирование работы и ошибок
Dataclasses	Работа с классами данных
JSON	Обработка ответов API
Структура проекта
text
weather-etl-pipeline/
│
├── db_weather_info/
│   └── База данных SQLite (создаётся локально)
│
├── ETL_WEATHER_PIPELINE.py   # Основной ETL-пайплайн
│
├── .env                      # API-ключ (не загружается в Git)
├── .gitignore                # Исключаемые из Git файлы
├── requirements.txt          # Зависимости проекта
└── README.md                 # Документация проекта

Установка и запуск
1. Клонирование репозитория
bash
git clone https://github.com/USERNAME/weather-etl-pipeline.git

cd weather-etl-pipeline

2. Создание виртуального окружения
bash
python -m venv venv


Активация виртуального окружения:

Windows:

bash
venv\Scripts\activate


Linux / macOS:

bash
source venv/bin/activate

3. Установка зависимостей
bash
pip install -r requirements.txt

4. Настройка переменных окружения

Создайте файл .env в корневой директории проекта:

env
API_KEY=your_openweathermap_api_key


Замените your_openweathermap_api_key на собственный API-ключ OpenWeatherMap.

5. Запуск ETL-пайплайна

Запуск с координатами по умолчанию:

bash
python ETL_WEATHER_PIPELINE.py


Запуск с собственными координатами и языком:

bash
python ETL_WEATHER_PIPELINE.py 40.7128 -74.0060 ru


Координаты по умолчанию соответствуют Нью-Йорку.

База данных

Обработанные погодные данные сохраняются в SQLite.

Таблица weather содержит следующие поля:

Столбец	Описание
ID	Уникальный идентификатор записи
LAT	Широта
LON	Долгота
DESCRIPTION	Описание погодных условий
TEMP	Температура (°C)
FEELS_LIKE	Ощущаемая температура (°C)
PRESSURE	Атмосферное давление (гПа)
HUMIDITY	Относительная влажность (%)
CLOUDS	Облачность (%)
TIME	Время наблюдения (UTC)
COUNTRY	Код страны
Источник данных

Погодные данные предоставляются через OpenWeatherMap API.
