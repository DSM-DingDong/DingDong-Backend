from datetime import datetime

from flask import Blueprint, Response, abort, current_app, request
from flask_restful import Api
from werkzeug.security import generate_password_hash

from app.models.account import AccountModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/check/id/<id>')
class IDCheck(BaseResource):
    def get(self, id):
        """
        자체 계정 ID 중복체크
        """
        return Response('', 409 if AccountModel.objects(id=id) else 200)


@api.resource('/signup')
class Signup(BaseResource):
    @json_required({'id': str, 'pw': str})
    def post(self):
        """
        자체 계정 회원가입
        """
        payload = request.json

        id = payload['id']

        if AccountModel.objects(id=id):
            abort(409)
        else:
            AccountModel(
                id=id,
                pw=generate_password_hash(payload['pw'])
            ).save()

            return Response('', 201)


@api.resource('/initialize/info/<id>')
class InitializeInfo(BaseResource):
    @json_required({'shortestCycle': int, 'longestCycle': int, 'lastMensStartDate': str, 'todayStatus': int})
    def post(self, id):
        """
        기본 정보 업로드
        """
        payload = request.json

        shortest_cycle = payload['shortestCycle']
        longest_cycle = payload['longestCycle']
        today_status = payload['todayStatus']

        account = AccountModel.objects(id=id).first()

        if not account:
            return Response('', 204)

        if all([account.shortest_cycle, account.longest_cycle, account.last_mens_start_date]):
            return Response('', 208)

        if shortest_cycle > longest_cycle:
            abort(400)

        account.update(
            shortest_cycle=shortest_cycle,
            longest_cycle=longest_cycle,
            last_mens_start_date=datetime.strptime(payload['lastMensStartDate'], '%Y-%m-%d'),
            calendar={str(datetime.now().date()): today_status}
        )

        redis_client = current_app.config['REDIS_CLIENT']
        redis_client.lpush('queue:requires_calendar_refresh', id)

        return Response('', 201)
