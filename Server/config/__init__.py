from datetime import timedelta
import os

import ujson


class Config:
    SERVICE_NAME = 'DingDong'
    SERVICE_NAME_UPPER = SERVICE_NAME.upper()
    REPRESENTATIVE_HOST = None

    RUN_SETTING = {
        'threaded': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    # Secret key for any 3-rd party libraries

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_HEADER_TYPE = 'JWT'

    MONGODB_SETTINGS = {
        'db': SERVICE_NAME,
        'host': None,
        'port': None,
        'username': None,
        'password': os.getenv('MONGO_PW_{}'.format(SERVICE_NAME_UPPER))
    }

    REDIS_SETTINGS = {
        'host': 'localhost',
        'port': 6379,
        'password': os.getenv('REDIS_PW_{}'.format(SERVICE_NAME_UPPER)),
        'db': 0
    }

    INFLUXDB_SETTINGS = {
        'host': 'localhost',
        'port': 8086,
        'username': 'root',
        'password': os.getenv('INFLUX_PW_{}'.format(SERVICE_NAME_UPPER), 'root'),
        'database': SERVICE_NAME
    }
