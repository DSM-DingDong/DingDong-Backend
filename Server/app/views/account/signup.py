from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


class IDCheck(BaseResource):
    def get(self):
        """
        ID 중복체크
        """


class Signup(BaseResource):
    def post(self):
        """
        자체 계정 회원가입
        """


class InitializeInfo(BaseResource):
    def post(self):
        """
        기본 정보 업로드
        """
