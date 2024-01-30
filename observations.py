import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

dbname = os.getenv('PG_DB')
user = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')
host = os.getenv('PG_HOST')
port =os.getenv('PG_PORT')

url_string = f"dbname={dbname} user={user} password={password} host={host} port={port}"

connection = psycopg2.connect(url_string)


def get_all_observations_sample():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
SELECT
    hf.station,
    loc.station_name,
    loc.state,
    hf.time,
    EXTRACT(YEAR from hf.time) AS rdg_year,
    EXTRACT(MONTH from hf.time) AS rdg_month,
    EXTRACT(DAY from hf.time) AS rdg_day,
    hf.temp_f,
    hf.pressure_in,
    hf.wind_mph,
    hf.precip_in,
    hf.humidity,
    hf.cloud
FROM hourlyforecasts hf
JOIN locations loc
    ON hf.station = loc.station
JOIN regions rgn
    ON loc.state = rgn.state
ORDER BY hf.station, hf.time
LIMIT 500;
'''
                )
            observations = cursor.fetchall()
            if observations:
                result = []
                for observation in observations:
                    result.append({
                        "station": observation[0],
                        "station_name": observation[1],
                        "state": observation[2],
                        "date": observation[3],
                        "rdg_year": observation[4],
                        "rdg_month": observation[5],
                        "rdg_day": observation[6],
                        "tmp": observation[7],
                        "slp": observation[8],
                        "wnd": observation[9],
                        "humidity": observation[10],
                        "cloud": observation[11],
                        })
                return result
            else:
                return f"Error, Observations not found, 404."


def get_all_stations():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
SELECT
    rgn.region,
    rgn.sub_region,
    loc.state,
    hf.station,
    loc.station_name
FROM hourlyforecasts hf
JOIN locations loc
    ON hf.station = loc.station
JOIN regions rgn
    ON loc.state = rgn.state
GROUP BY 1, 2, 3, 4, 5
ORDER BY 1, 2, 3, 5;
'''
                ) 
            stations = cursor.fetchall()
            if stations:
                result = []
                for station in stations:
                    result.append({
                        "region": station[0],
                        "sub_region": station[1],
                        "state": station[2],
                        "station": station[3],
                        "station_name": station[4],
                         })
                return result
            else:
                return f"Error, Stations not found, 404."


def get_all_dates():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
SELECT
    EXTRACT(YEAR from hf.time) AS rdg_year,
    EXTRACT(MONTH from hf.time) AS rdg_month,
    EXTRACT(DAY from hf.time) AS rdg_day,
    DATE(hf.time) AS date
FROM hourlyforecasts hf
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2, 3;
'''
                ) 
            dates = cursor.fetchall()
            if dates:
                result = []
                for date in dates:
                    result.append({
                        "rdg_year": date[0],
                        "rdg_month": date[1],
                        "rdg_day": date[2],
                        "date": date[3],
                         })
                return result
            else:
                return f"Error, Dates not found, 404."


def get_all_stationid(stationid):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
SELECT
    hf.station,
    loc.station_name,
    loc.state,
    hf.time,
    EXTRACT(YEAR from hf.time) AS rdg_year,
    EXTRACT(MONTH from hf.time) AS rdg_month,
    EXTRACT(DAY from hf.time) AS rdg_day,
    hf.temp_f,
    hf.pressure_in,
    hf.wind_mph,
    hf.precip_in,
    hf.humidity,
    hf.cloud
FROM hourlyforecasts hf
JOIN locations loc
    ON hf.station = loc.station
JOIN regions rgn
    ON loc.state = rgn.state
WHERE hf.station = %s
ORDER BY hf.station, hf.time;
'''
            , (stationid,)) 
            observations = cursor.fetchall()
            if observations:
                result = []
                for observation in observations:
                    result.append({
                        "station": observation[0],
                        "station_name": observation[1],
                        "state": observation[2],
                        "date": observation[3],
                        "rdg_year": observation[4],
                        "rdg_month": observation[5],
                        "rdg_day": observation[6],
                        "tmp": observation[7],
                        "slp": observation[8],
                        "wnd": observation[9],
                        "humidity": observation[10],
                        "cloud": observation[11],
                        })
                return result
            else:
                return f"Error, Observations with Station ID {stationid} not found, 404."


def get_all_date(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:])
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                 f'''
SELECT
    hf.station,
    loc.station_name,
    loc.state,
    hf.time,
    EXTRACT(YEAR from hf.time) AS rdg_year,
    EXTRACT(MONTH from hf.time) AS rdg_month,
    EXTRACT(DAY from hf.time) AS rdg_day,
    hf.temp_f,
    hf.pressure_in,
    hf.wind_mph,
    hf.precip_in,
    hf.humidity,
    hf.cloud
FROM hourlyforecasts hf
JOIN locations loc
    ON hf.station = loc.station
JOIN regions rgn
    ON loc.state = rgn.state
WHERE EXTRACT(year from time) = {year}
    AND EXTRACT(month from time) = {month}
    AND EXTRACT (day from time) = {day}
ORDER BY hf.station, hf.time;
'''
                 )
            observations = cursor.fetchall()
            if observations:
                result = []
                for observation in observations:
                    result.append({
                        "station": observation[0],
                        "station_name": observation[1],
                        "state": observation[2],
                        "date": observation[3],
                        "rdg_year": observation[4],
                        "rdg_month": observation[5],
                        "rdg_day": observation[6],
                        "tmp": observation[7],
                        "slp": observation[8],
                        "wnd": observation[9],
                        "humidity": observation[10],
                        "cloud": observation[11],
                        })
                return result
            else:
                return f"Error, records with Date {date} not found, 404."
