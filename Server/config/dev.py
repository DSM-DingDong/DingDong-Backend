from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True

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
