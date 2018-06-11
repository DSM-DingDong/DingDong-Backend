from datetime import datetime
from uuid import uuid4

from flask import Blueprint, current_app, g, request
from flask_restful import Api

from app.models.account import AccountModel
from app.models.data import VoiceModel
from app.views import BaseResource, auth_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/voice')
class MainInfo(BaseResource):
    @auth_required(AccountModel)
    def post(self):
        user = g.user

        file = request.files['file']

        while True:
            filename = str(uuid4())

            if not VoiceModel.objects(filename=filename):
                VoiceModel(
                    date=str(datetime.now().date()),
                    owner=user,
                    filename=filename
                )

                file.save('../../voice-files/{}'.format(filename))

                if not current_app.testing:
                    kafka_producer = current_app.config['KAFKA_PRODUCER']
                    kafka_producer.send('id_needs_calendar_refresh', {'id': id})

                break
