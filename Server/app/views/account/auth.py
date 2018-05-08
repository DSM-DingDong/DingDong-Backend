from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


class Auth(BaseResource):
    def post(self):
        """
        자체 계정 로그인
        """


class FacebookAuth(BaseResource):
    def post(self):
        """
        페이스북 계정 로그인
        """


class Refresh(BaseResource):
    def post(self):
        """
        Access token refresh
        """
