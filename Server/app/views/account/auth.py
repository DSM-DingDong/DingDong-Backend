from uuid import uuid4

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import create_access_token
from flask_restful import Api
from werkzeug.security import check_password_hash

from app.models.account import SystemAccountModel, FacebookAccountModel, RefreshTokenModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


def create_refresh_token(owner):
    from flask_jwt_extended import create_refresh_token

    while True:
        uuid = uuid4()

        if not RefreshTokenModel.objects(token=uuid):
            RefreshTokenModel(token=uuid, pw_snapshot=owner.pw, owner=owner).save()

            return create_refresh_token(uuid)


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

        account = SystemAccountModel.objects(id=id).first()

        if not account:
            abort(401)
        else:
            if check_password_hash(account.pw, pw):
                if not all([account.shortest_cycle, account.longest_cycle, account.last_mens_start_date]):
                    return Response('', 204)
                else:
                    return {
                        'accessToken': create_access_token(account.id),
                        'refreshToken': create_refresh_token(account)
                    }


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
