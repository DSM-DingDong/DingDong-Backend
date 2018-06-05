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
        if AccountModel.objects(id=id):
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
        payload = request.json

        id = payload['id']
        pw = payload['pw']

        if AccountModel.objects(id=id):
            abort(409)
        else:
            AccountModel(
                id=id,
                pw=generate_password_hash(pw)
            ).save()

            return Response('', 201)


@api.resource('/initialize/info/<id>')
class InitializeInfo(BaseResource):
    @json_required({'shortestCycle': int, 'longestCycle': int, 'lastMensStartDate': str})
    def post(self, id):
        """
        기본 정보 업로드
        """
        payload = request.json

        shortest_cycle = payload['shortestCycle']
        longest_cycle = payload['longestCycle']
        last_mens_start_date = datetime.strptime(payload['lastMensStartDate'], '%Y-%m-%d')

        account = AccountModel.objects(id=id).first()

        if not account:
            return Response('', 204)

        if all([account.shortest_cycle, account.longest_cycle, account.last_mens_start_date]):
            return Response('', 201)

        if shortest_cycle > longest_cycle:
            abort(400)

        account.update(
            shortest_cycle=shortest_cycle,
            longest_cycle=longest_cycle,
            last_mens_start_date=last_mens_start_date
        )

        if not current_app.testing:
            kafka_producer = current_app.config['KAFKA_PRODUCER']
            kafka_producer.send('id_needs_calendar_refresh', {'id': id})

        return Response('', 201)
