from datetime import datetime
from unittest import TestCase as TC

import pymongo
from flask import Response
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash

from app import create_app
from app.models.account import AccountModel, TokenModel, AccessTokenModel, RefreshTokenModel

from config.test import TestConfig

app = create_app(TestConfig)


class TCBase(TC):
    mongo_setting = app.config['MONGODB_SETTINGS']
    db_name = mongo_setting.pop('db')
    mongo_client = pymongo.MongoClient(**mongo_setting)
    mongo_setting['db'] = db_name

    def __init__(self, *args, **kwargs):
        self.app = app
        self.client = self.app.test_client()
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.token_regex = '([\w\-\_]+\.){2}[\w\-\_]+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.primary_user = AccountModel(
            id='primary_user',
            pw=self.encrypted_primary_user_pw,
            shortest_cycle=25,
            longest_cycle=35,
            last_mens_start_date=datetime(2018, 5, 15)
        ).save()

        self.secondary_user = AccountModel(
            id='secondary_user',
            pw=self.encrypted_secondary_user_pw,
            shortest_cycle=28,
            longest_cycle=32,
            last_mens_start_date=datetime(2018, 5, 20)
        ).save()

    def _generate_tokens(self):
        with app.app_context():
            self.primary_user_access_token = create_access_token(TokenModel.generate_token(AccessTokenModel, self.primary_user))
            self.primary_user_refresh_token = create_refresh_token(TokenModel.generate_token(RefreshTokenModel, self.primary_user))

            self.secondary_user_access_token = create_access_token(TokenModel.generate_token(AccessTokenModel, self.secondary_user))
            self.secondary_user_refresh_token = create_refresh_token(TokenModel.generate_token(RefreshTokenModel, self.secondary_user))

    def setUp(self):
        self.primary_user_pw = self.secondary_user_pw = 'pw'

        self.encrypted_primary_user_pw = generate_password_hash(self.primary_user_pw)
        self.encrypted_secondary_user_pw = generate_password_hash(self.secondary_user_pw)

        self._create_fake_account()
        self._generate_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)

    def request(self, method, target_url_rule, token=None, *args, **kwargs):
        """
        Helper for common request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        return method(
            target_url_rule,
            headers={'Authorization': token or self.primary_user_access_token},
            *args,
            **kwargs
        )
