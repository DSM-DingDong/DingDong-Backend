import socket

from config import Config


class ProductionConfig(Config):
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 1024
    DEBUG = False

    RUN_SETTING = dict(Config.RUN_SETTING, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    MONGODB_SETTINGS = {
        'db': Config.SERVICE_NAME,
        'username': None,
        'password': None
    }

    KAFKA_BROKERS = (
        'localhost:9092'
    )

    INFLUX_DB_SETTINGS = {
        'db': Config.SERVICE_NAME.replace('-', '_')
    }
