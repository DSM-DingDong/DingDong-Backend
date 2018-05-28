from uuid import uuid4

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import create_access_token
from flask_restful import Api
from werkzeug.security import check_password_hash

from app.models.account import AccountModel, TokenModel, AccessTokenModel, RefreshTokenModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/auth/common')
class Auth(BaseResource):
    @json_required({'id': str, 'pw': str})
    def post(self):
        """
        자체 계정 로그인
        """
        payload = request.json

        id = payload['id']
        pw = payload['pw']

        user = AccountModel.objects(id=id).first()

        if not user:
            abort(401)
        else:
            if check_password_hash(user.pw, pw):
                if not all([user.shortest_cycle, user.longest_cycle, user.last_mens_start_date]):
                    return Response('', 204)
                else:
                    return {
                        'accessToken': TokenModel.generate_token(AccessTokenModel, account),
                        'refreshToken': TokenModel.generate_token(RefreshTokenModel, account)
                    }
            else:
                abort(401)


@api.resource('/auth/facebook')
class FacebookAuth(BaseResource):
    def post(self):
        """
        페이스북 계정 로그인
        """


@api.resource('/refresh')
class Refresh(BaseResource):
    def post(self):
        """
        Access token refresh
        """
