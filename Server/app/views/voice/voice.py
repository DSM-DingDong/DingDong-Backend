import os
from datetime import date

from flask import Blueprint, Response, current_app, g, request
from flask_restful import Api
from pydub import AudioSegment

from app.models.account import AccountModel
from app.views import BaseResource, auth_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/voice')
class MainInfo(BaseResource):
    MP3_FILE_DIR = 'voice-files'

    @auth_required(AccountModel)
    def post(self):
        file = request.files['file']

        today = str(date.today())

        filename = '{}_{}.mp3'.format(today, g.user.id)

        file.save(os.path.join(self.MP3_FILE_DIR, filename))

        song = AudioSegment.from_mp3('{}/{}'.format(self.MP3_FILE_DIR, filename))
        song.export('{}/{}.wav'.format(self.MP3_FILE_DIR, filename[:-4]), format='wav')
        os.remove('{}/{}'.format(self.MP3_FILE_DIR, filename))

        redis_client = current_app.config['REDIS_CLIENT']
        redis_client.lpush('queue:requires_calendar_refresh', g.user.id)

        return Response('', 201)
