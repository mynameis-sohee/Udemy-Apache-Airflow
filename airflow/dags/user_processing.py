from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime

# 파라미터 정의

default_args = {
    'start_date': datetime(2021, 8, 1)
}

# start_date : 실제로 데이터 파이프라인이 예약되기 시작하는 날짜
with DAG('user_processing', schedule_interval='@daily',
default_args=default_args, catchup=False) as dag:
    # task 및 operators 정의

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )