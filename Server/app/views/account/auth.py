import requests
import ujson

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import create_access_token, create_refresh_token
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
                        'accessToken': create_access_token(TokenModel.generate_token(AccessTokenModel, user)),
                        'refreshToken': create_refresh_token(TokenModel.generate_token(RefreshTokenModel, user))
                    }
            else:
                abort(401)


@api.resource('/auth/facebook')
class FacebookAuth(BaseResource):
    FB_GRAPH_API_URL = 'https://graph.facebook.com/v2.6/{}?access_token=1925974487664670|D-wibfbjkOaHtINm_cwUSBx38k8'

    def is_available_fb_id(self, fb_id):
        resp = requests.get(self.FB_GRAPH_API_URL.format(fb_id))
        # 페이스북 graph api를 이용해 사용자 데이터 조회

        data = ujson.loads(resp.text)

        return False if 'error' in data else True

    @json_required({'fbId': str})
    def post(self):
        """
        페이스북 계정 로그인
        """
        payload = request.json

        fb_id = payload['fbId']

        user = AccountModel.objects(id=fb_id).first()

        if not user:
            # 사용자가 미존재, 회원가입을 함께 시켜줌
            if self.is_available_fb_id(fb_id):
                AccountModel(
                    id=fb_id
                ).save()
            else:
                abort(401)

        return {
            'accessToken': create_access_token(TokenModel.generate_token(AccessTokenModel, user)),
            'refreshToken': create_refresh_token(TokenModel.generate_token(RefreshTokenModel, user))
        }


@api.resource('/refresh')
class Refresh(BaseResource):
    def post(self):
        """
        Access token refresh
        """
