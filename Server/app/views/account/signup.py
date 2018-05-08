from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from werkzeug.security import generate_password_hash

from app.models.account import AccountBase, SystemAccountModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/check/id/<id>')
class IDCheck(BaseResource):
    def get(self, id):
        """
        자체 계정 ID 중복체크
        """
        if SystemAccountModel.objects(id=id):
            # 중복됨
            abort(409)
        else:
            # 중복되지 않음
            return Response('', 200)


@api.resource('/signup')
class Signup(BaseResource):
    @json_required({'id': str, 'pw': str})
    def post(self):
        """
        자체 계정 회원가입
        """
        id = request.json['id']
        pw = request.json['pw']

        if SystemAccountModel.objects(id=id):
            abort(409)
        else:
            SystemAccountModel(
                id=id,
                pw=generate_password_hash(pw)
            ).save()

            return Response('', 201)

class InitializeInfo(BaseResource):
    def post(self):
        """
        기본 정보 업로드
        """
