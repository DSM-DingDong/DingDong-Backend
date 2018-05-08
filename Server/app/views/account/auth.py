from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from
from werkzeug.security import check_password_hash

from app.models.account import SystemAccountModel, FacebookAccountModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


class Auth(BaseResource):
    @json_required({'id': str, 'pw': str})
    def post(self):
        """
        자체 계정 로그인
        """
        id = request.json['id']
        pw = request.json['pw']

        account = SystemAccountModel.objects(id=id).first()

        if not account:
            abort(401)
        else:
            # TODO
            pass


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
