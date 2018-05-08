from kafka import KafkaProducer
import ujson

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
    Mongo().init_app(app_)
    Router().init_app(app_)

    kafka_producer = KafkaProducer(
        bootstrap_servers=app_.config['KAFKA_BROKERS'],
        value_serializer=lambda v: ujson.dumps(v).encode('utf-8')
    )

    app_.config['KAFKA_PRODUCER'] = kafka_producer

    return app_
