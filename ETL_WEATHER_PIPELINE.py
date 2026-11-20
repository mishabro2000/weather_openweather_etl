# импортируем библиотеки
import logging
import datetime
import sys
import os
import sqlite3
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from contextlib import closing
from dataclasses import dataclass
# настраиваем логирование
logging.basicConfig(
    level = logging.INFO,
    filename = 'history_weather_ETL.log',
    filemode = 'a',
    encoding = 'utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s'
    )
# подключаем переменные окружения для .env
load_dotenv()

def adapt_datetime(dt):
    return dt.isoformat()

#Конвертер: как превратить строку из SQLite обратно в объект datetime в Python
def convert_datetime(val):
    return datetime.datetime.fromisoformat(val.decode())

# Регистрируем их в sqlite3
sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)
# Класс для извлечения данных
@dataclass
class ExtractWeather:
    # параметры,сначала идут те которые мы берем из сайта а другие сами добавляем
    lat: float
    lon: float
    lang: str
    units: str = 'metric'
    url: str = 'https://api.openweathermap.org/data/2.5/weather'
    appid: str = os.environ.get("API_KEY")
    # проводим в dataclass проверку на API-ключ и на координаты
    def __post_init__(self):
        if not self.appid:
            logging.critical("API-Ключ не найден!")
            raise ValueError("не найден файл .env с ключом либо в файле опечатка")
        
        if not -90 <= self.lat <= 90:
            logging.critical("некорректное значение широты")
            raise ValueError("некорректное значение широты")
        
        if not -180 <= self.lon <= 180:
            logging.critical("некорректное значение долготы")
            raise ValueError("некорректное значение долготы")

    # базовая защита(проверка и ожидание)
    @retry(stop = stop_after_attempt(3),wait = wait_fixed(5))
    def fetch_raw_data(self) -> dict:
        # параметры для запроса
        params = {

        'lat': self.lat,      
        'lon': self.lon,          
        'appid': self.appid,    
        'units': self.units,        
        'lang': self.lang             
    }
        try:
            # делаем запрос и запрашиваем статус сервера и передаем данные в следующий класс
            response = requests.get(self.url,params,timeout = 10)
            response.raise_for_status()
            logging.info("Данные были успешно извлечены и передаються в следующий класс для их обработки")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API error: {e}")
            raise


class TransformWeather:
    def __init__(self):
        pass
    # очистка данных
    def clean_data(self,raw_data):

        try:
            # создаем список для хранения очищенных данных 
            clean_data_weather = []

            logging.info("начало отчистки данных")
            # Извлекаем географические координаты из исходного JSON
            coords = raw_data.get('coord', {})
            # получаем данные и преобразуем их в дробное число и так со всеми данными
            lat = coords.get('lat')
            if lat is not None:
                lat = float(lat)
        
            lon = coords.get('lon')
            if lon is not None:
                lon = float(lon)
            # извлекаем данные из списка где собранна информация про погоду
            weathers = raw_data.get('weather', [])
            # инциализируем описание
            description = None
            # если список не пустой то берем данные и преобразуем их в строку и ставим в нижний регистр
            if weathers:
                raw_data.get('weather',[])
                description = weathers[0].get('description')
                if description is not None:
                    description = str(description).lower()
            
            mains = raw_data.get('main',{})
            temp = mains.get('temp')
            if temp is not None:
                temp = float(temp)
                if not(-89.2 <= temp <= 56.7):
                    logging.error(f"нереальная температура:{temp}")
                    return[]

            feels_like = mains.get('feels_like')
            if feels_like is not None:
                feels_like = float(feels_like)
                if not (-112.2 <= feels_like <= 80.7):
                    logging.error(f"нереальная температура:{feels_like} вы попросту сгорите/замерзните")
                    return[]
                
            pressure = mains.get('pressure')
            if pressure is not None:
                pressure = float(pressure)
                if not (850.0 < pressure <= 1085.6):
                    logging.warning("связи с тем что эти данные являются не корректными и мы их переформатируем ")
                    pressure = None

            humidity = mains.get('humidity')
            if humidity is not None:
                humidity = float(humidity)
                if not(0.03 < humidity <= 100.0):
                    logging.warning("связи с тем что эти данные являются не корректными и мы их переформатируем ")
                    humidity = None

            clouds = raw_data.get('clouds',{})
            cloud = clouds.get('all')
            if cloud is not None:
                cloud = float(cloud)
                if not(0.0 <= cloud <= 100.0):
                    logging.warning("связи с тем что эти данные являются не корректными и мы их переформатируем и они будут равны нулю")
                    cloud = None

            dt = raw_data.get('dt')
            if dt is not None:
                dt = datetime.datetime.fromtimestamp(dt, datetime.timezone.utc)

            s = raw_data.get('sys',{})
            sys = s.get('country')
            if sys is not None:
                sys = str(sys).upper()
            # создаем кортеж и добавляем его в список
            weathers_cuple = (lat,lon,description,temp,feels_like,pressure,humidity,cloud,dt,sys)
            clean_data_weather.append(weathers_cuple)


        except Exception as e:
            logging.error(f"Ошибка:{e}")
            raise

        logging.info("Данные были успешно очищены и передаються в следующий класс для их загрузки в базу данных")
        return clean_data_weather
        
class LoadWeather:
    def __init__(self,db_path = 'db_weather',db_dir = "db_weather_info",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES):

        self.db_path = db_path
        self.detect_types = detect_types
        self.db_dir = db_dir
        # проверяем существует ли директория если нет то создаем
        if not os.path.exists(self.db_dir):
            os.makedirs(db_dir)
            logging.info(f"Директория {self.db_dir} была успешно создана")
        # создаем полный путь к файлу для дальнейшей записи
        self.db_path = os.path.join(db_dir,db_path)

    def load_data(self,clean_data_weather):

        if not clean_data_weather:
            logging.warning("в списке нету данных!")
            return
        # открываем безопасное соеденение с базой данных
        with closing(sqlite3.connect(self.db_path,detect_types = self.detect_types)) as conn:
            with conn:
                cur = conn.cursor()
                # создаем таблицу
                cur.execute("""
                CREATE TABLE IF NOT EXISTS weather(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LAT REAL,
                LON REAL,
                DESCRIPTION TEXT,
                TEMP REAL,
                FEELS_LIKE REAL,
                PRESSURE REAL,
                HUMIDITY REAL,
                CLOUDS REAL,
                TIME TIMESTAMP,
                COUNTRY TEXT,
                UNIQUE(LAT, LON, TIME)
            )
    """)

                try:
                    #вставляем данные в нашу базу данных
                    cur.executemany("INSERT OR IGNORE INTO weather(LAT,LON,DESCRIPTION,TEMP,FEELS_LIKE,PRESSURE,HUMIDITY,CLOUDS,TIME,COUNTRY) VALUES(?,?,?,?,?,?,?,?,?,?)",clean_data_weather)
                    logging.info("данные были успешно внесены в базу данных о погоде")

                except Exception as e:
                    logging.error(f"ошибка данные не внесены в базу данных {e}")
                    raise
                # просим показать сколько записей было внесено в базу
                cur.execute("SELECT COUNT(*) FROM weather")
                rows = cur.fetchone()[0]
                logging.info("Выгрузка прошла успешно,общее кол-во записей составляет %s",rows)

if __name__ == '__main__':
    # координаты нью-йорка на случай если пользователь ничего не будет изменять и ставить собственные координаты
    DEFAULT_LAT = 40.7128
    DEFAULT_LON = -74.0060

    lat_sys = DEFAULT_LAT
    lon_sys = DEFAULT_LON 
    speak = 'ru'
    # проверяем на ошибки в передачи аргументов 
    if len(sys.argv) == 2 or len(sys.argv) > 4:
        sys.stderr.write("Ошибка.Надо указать <название программы .py> <широта> <долгота> <язык> \n")
        sys.exit(1)

    if len(sys.argv) == 1:
        sys.stdout.write("по умолчанию будут использованы кординаты нью-йорка а язык выбран русский\n")
    # проверяем переданные параметры либо 2 аргумента либо 3
    if len(sys.argv) in (3,4):
        # если параметры переданы в количестве 2
        try:
            temp_lat = float(sys.argv[1])
            temp_lon = float(sys.argv[2])

            lat_sys = temp_lat
            lon_sys = temp_lon
            # есчли переданно 3 аргумента
            if len(sys.argv) == 4:
                speak = sys.argv[3].lower()
            sys.stdout.write("параметры для запроса успешно приняты \n")
        except ValueError:
            logging.warning(f"неверные переданные параметры для запроса,будут переданы параметры по умолчанию")

    logging.info(f"Запуск ETL со следующими параметрами широта:{lat_sys} долгота:{lon_sys} язык:{speak}")
    # присваеваем значения классов переменным для конвеера
    E = ExtractWeather(lat = lat_sys,lon = lon_sys,lang = speak)
    T = TransformWeather()
    L = LoadWeather(db_path = "db_weather")

    try:
        # создаем конвеер
        raw_data = E.fetch_raw_data()
        clean_data = T.clean_data(raw_data)
        L.load_data(clean_data)

    except Exception as e:
        logging.error(f"!!! ПАЙПЛАЙН УПАЛ С ОШИБКОЙ: {e} !!!")
        raise

    logging.info("ETL-пайплан завершен успешно!")
