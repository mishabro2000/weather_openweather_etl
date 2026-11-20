# 🌦️ OpenWeather ETL Pipeline

[![English](https://shields.io)](#english)
[![Русский](https://shields.io)](#русский)

---

<a name="english"></a>
## 🇬🇧 English Version

A reliable and fault-tolerant Python ETL pipeline designed to extract, validate, and store meteorological data from the **OpenWeather API** into a relational **SQLite** database.

> **About the Author:** Hi! I'm a 15-year-old aspiring Data Engineer passionate about building clean, production-grade data pipelines, data quality validation, and backend architecture. This project demonstrates OOP principles with a strict separation of concerns across Extract, Transform, and Load stages.

### 🛠 Tech Stack

* **Python 3.10+** (`dataclasses`, `sqlite3`, `logging`, `datetime`, `sys`)
* **Requests** — HTTP requests to the REST API
* **Tenacity** — automatic retries with fixed delays on network failures
* **Python-dotenv** — secure management of secrets and environment variables
* **SQLite3** — lightweight relational storage with custom `TIMESTAMP` type adapters
* **Pytest** — unit testing for pipeline components

### 🏗 Project Architecture

The pipeline is decoupled into three independent classes:

1. **`ExtractWeather` (`@dataclass`)**
   * Validates the presence of `API_KEY` upon initialization (`__post_init__`).
   * Executes GET requests to the OpenWeather Current Weather API with timeouts and network resilience (`tenacity`).
2. **`TransformWeather`**
   * Flattens the nested JSON structure returned by the API.
   * Converts Unix Timestamps into timezone-aware `datetime` objects (strictly in **UTC**).
   * Performs **Data Quality** validation on physical metrics (rejecting anomalous temperatures and softly nullifying out-of-bounds pressure, humidity, and cloudiness values).
3. **`LoadWeather`**
   * Automatically creates the target directory and database schema in SQLite.
   * Ensures **idempotency** using a composite unique constraint `UNIQUE(LAT, LON, TIME)` combined with `INSERT OR IGNORE` to prevent duplicate records on repeated runs.

### 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mishabro2000/weather_openweather_etl
   cd weather-etl-pipeline
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # For Windows:
   venv\Scripts\activate
   # For Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root and add your OpenWeather API key:
   ```env
   API_KEY=your_secret_openweather_api_key
   ```

### 💻 Usage Examples

The script supports command-line arguments (CLI) with atomic fallback to default settings if invalid input is provided:

* **Run with default settings** (New York: `40.7128, -74.0060`, language: `ru`):
  ```bash
  python ETL_WEATHER_PIPELINE.py
  ```

* **Run for specific coordinates** (e.g., Moscow, default language `ru`):
  ```bash
  python ETL_WEATHER_PIPELINE.py 55.7558 37.6173
  ```

* **Run with custom coordinates and weather description language** (e.g., London, `en`):
  ```bash
  python ETL_WEATHER_PIPELINE.py 51.5074 -0.1278 en
  ```

### 🗄 SQLite Table Schema (`weather`)

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `ID` | `INTEGER` | Primary key (`PRIMARY KEY AUTOINCREMENT`) |
| `LAT` | `REAL` | Location latitude (part of the unique key) |
| `LON` | `REAL` | Location longitude (part of the unique key) |
| `DESCRIPTION` | `TEXT` | Text description of weather conditions |
| `TEMP` | `REAL` | Air temperature (°C) |
| `FEELS_LIKE` | `REAL` | Perceived temperature (°C) |
| `PRESSURE` | `REAL` | Atmospheric pressure (hPa) |
| `HUMIDITY` | `REAL` | Relative air humidity (%) |
| `CLOUDS` | `REAL` | Cloudiness (%) |
| `TIME` | `TIMESTAMP` | Measurement timestamp in ISO 8601 format (UTC) |
| `COUNTRY` | `TEXT` | Two-letter country code (ISO 3166) |

### 📊 Logging & Testing

* All pipeline execution stages, Data Quality warnings, and errors are logged to `history_weather_ETL.log`.
* To run unit tests, execute:
  ```bash
  pytest
  ```

---

<a name="русский"></a>
## 🇷🇺 Русская версия

Надёжный и отказоустойчивый ETL-пайплайн на Python для сбора, валидации и сохранения метеорологических данных из **OpenWeather API** в реляционную базу данных **SQLite**.

> **Об авторе:** Привет! Мне 15 лет, я начинающий Data Engineer и увлекаюсь построением чистых, отказоустойчивых конвейеров данных, валидацией качества данных (Data Quality) и проектированием архитектуры. Этот проект построен на принципах ООП с чётким разделением ответственности между этапами извлечения, трансформации и загрузки данных.

### 🛠 Технологический стек

* **Python 3.10+** (`dataclasses`, `sqlite3`, `logging`, `datetime`, `sys`)
* **Requests** — HTTP-запросы к REST API
* **Tenacity** — автоматические повторные попытки (retries) при сетевых сбоях
* **Python-dotenv** — безопасное управление секретами и переменными окружения
* **SQLite3** — хранение данных с кастомными адаптерами типов `TIMESTAMP`
* **Pytest** — модульное тестирование компонентов пайплайна

### 🏗 Архитектура проекта

Пайплайн разделён на три независимых класса:

1. **`ExtractWeather` (`@dataclass`)**
   * Валидирует наличие `API_KEY` при инициализации (`__post_init__`).
   * Выполняет GET-запросы к OpenWeather Current Weather API с таймаутом и защитой от временных сбоев сети (`tenacity`).
2. **`TransformWeather`**
   * «Выпрямляет» вложенную JSON-структуру ответа API.
   * Конвертирует Unix Timestamp в объекты `datetime` (строго в часовом поясе **UTC**).
   * Проводит **Data Quality** валидацию физических показателей (отбраковка аномальных температур, мягкая очистка некорректных значений давления, влажности и облачности).
3. **`LoadWeather`**
   * Автоматически создаёт директорию и схему таблицы в SQLite.
   * Обеспечивает **идемпотентность** загрузки за счёт составного уникального ключа `UNIQUE(LAT, LON, TIME)` и конструкции `INSERT OR IGNORE` (защита от дублей при повторных запусках).

### 🚀 Установка и настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/mishabro2000/weather_openweather_etl
   cd weather-etl-pipeline
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для Linux/macOS:
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта и добавьте ваш API-ключ от OpenWeather:
   ```env
   API_KEY=ваш_секретный_ключ_openweather
   ```

### 💻 Примеры запуска

Скрипт поддерживает передачу параметров через командную строку (CLI) с атомарным откатом к настройкам по умолчанию при некорректном вводе:

* **Запуск со значениями по умолчанию** (Нью-Йорк: `40.7128, -74.0060`, язык: `ru`):
  ```bash
  python ETL_WEATHER_PIPELINE.py
  ```

* **Запуск для конкретных координат** (например, Москва, язык по умолчанию `ru`):
  ```bash
  python ETL_WEATHER_PIPELINE.py 55.7558 37.6173
  ```

* **Запуск с указанием координат и языка описания погоды** (например, Лондон, `en`):
  ```bash
  python ETL_WEATHER_PIPELINE.py 51.5074 -0.1278 en
  ```

### 🗄 Структура таблицы в SQLite (`weather`)

| Колонка | Тип данных | Описание |
| :--- | :--- | :--- |
| `ID` | `INTEGER` | Первичный ключ (`PRIMARY KEY AUTOINCREMENT`) |
| `LAT` | `REAL` | Широта локации (часть уникального ключа) |
| `LON` | `REAL` | Долгота локации (часть уникального ключа) |
| `DESCRIPTION` | `TEXT` | Текстовое описание погодных условий |
| `TEMP` | `REAL` | Температура воздуха (°C) |
| `FEELS_LIKE` | `REAL` | Ощущаемая температура (°C) |
| `PRESSURE` | `REAL` | Атмосферное давление (гПа) |
| `HUMIDITY` | `REAL` | Относительная влажность воздуха (%) |
| `CLOUDS` | `REAL` | Облачность (%) |
| `TIME` | `TIMESTAMP` | Время замера в формате ISO 8601 (UTC) |
| `COUNTRY` | `TEXT` | Двухбуквенный код страны (ISO 3166) |

### 📊 Логирование и тесты

* Все этапы работы конвейера, предупреждения Data Quality и ошибки записываются в файл `history_weather_ETL.log`.
* Для запуска модульных тестов выполните:
  ```bash
  pytest
  ```
