from datetime import datetime

from flask import Blueprint, g
from flask_restful import Api

from app.models.account import AccountModel
from app.models.data import VoiceModel
from app.views import BaseResource, auth_required

api = Api(Blueprint(__name__, __name__))
api.prefix = '/info'


@api.resource('/main')
class MainInfo(BaseResource):
    @auth_required(AccountModel)
    def get(self):
        user = g.user

        today = str(datetime.now().date())

        calendar = user.calendar

        remission_available_start_date = None
        remission_available_end_date = None
        mens_start_date = None
        mens_end_date = None

        for idx, date in enumerate(calendar):
            if date < today:
                continue

            if calendar[idx - 1] != 2 and calendar[idx] == 2:
                remission_available_start_date = remission_available_start_date or date
                # 덮어쓰기 방지. 이미 데이터가 들어가 있다면 그대로 유지하도록

            elif calendar[idx - 1] == 2 and calendar[idx] != 2:
                remission_available_end_date = remission_available_end_date or date

            elif calendar[idx] == 3:
                mens_start_date = mens_start_date or date

            elif calendar[idx] == 5:
                mens_end_date = mens_end_date or date

            if all((remission_available_start_date, remission_available_end_date, mens_start_date, mens_end_date)):
                break

        return {
            'remissionAvailable': {
                'start': remission_available_start_date,
                'end': remission_available_end_date
            },
            'mens': {
                'start': mens_start_date,
                'end': mens_end_date
            },
            'needVoiceRecord': True if VoiceModel.objects(date=datetime.now().strftime('%Y-%m-%d'), owner=user) else False
        }
