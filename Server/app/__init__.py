from kafka import KafkaProducer
from influxdb import InfluxDBClient
from mongoengine import connect
from redis import Redis

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.models import Mongo
from app.views import Router


def create_app(*config_cls):
    """
    Creates Flask instance & initialize

    Returns:
        Flask
    """
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(__name__)

    for config in config_cls:
        app_.config.from_object(config)

    CORS().init_app(app_)
    JWTManager().init_app(app_)
    Router().init_app(app_)

    connect(**app_.config['MONGODB_SETTINGS'])
    if not app_.testing:
        app_.config['KAFKA_PRODUCER'] = KafkaProducer(**app_.config['KAFKA_SETTINGS'])
        
    app_.config['REDIS_CLIENT'] = Redis(**app_.config['REDIS_SETTINGS'])
    app_.config['INFLUXDB_CLIENT'] = InfluxDBClient(**app_.config['INFLUXDB_SETTINGS'])

    return app_
