import os
import wave
from datetime import datetime

from flask import Blueprint, Response, current_app, g, request
from flask_restful import Api
from pydub import AudioSegment
import numpy as np

from app.models.account import AccountModel
from app.views import BaseResource, auth_required

api = Api(Blueprint(__name__, __name__))
api.prefix = ''


@api.resource('/voice')
class UploadVoiceData(BaseResource):
    MP3_FILE_DIR = 'voice-files'

    @classmethod
    def extract_frequency_avg(cls, wav_filename, today):
        wr = wave.open('{}/{}'.format(cls.MP3_FILE_DIR, wav_filename))
        sz = wr.getnframes()
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2]
        lf, rf = np.absolute(np.fft.rfft(left)), np.absolute(np.fft.rfft(right))

        g.user.voice_avg[today] = (lf.argmin() + lf.argmax() + rf.argmin() + rf.argmax()) / 4
        g.user.save()

    @auth_required(AccountModel)
    def post(self):
        file = request.files['file']

        today = str(datetime.now().date())

        mp3_filename = '{}_{}.mp3'.format(today, g.user.id)
        file.save(os.path.join(self.MP3_FILE_DIR, mp3_filename))

        song = AudioSegment.from_mp3('{}/{}'.format(self.MP3_FILE_DIR, mp3_filename))

        wav_filename = mp3_filename[:-4] + '.wav'
        song.export('{}/{}.wav'.format(self.MP3_FILE_DIR, wav_filename[:-4]), format='wav')
        os.remove('{}/{}'.format(self.MP3_FILE_DIR, mp3_filename))

        self.extract_frequency_avg(wav_filename, today)

        redis_client = current_app.config['REDIS_CLIENT']
        redis_client.lpush('queue:requires_calendar_refresh', g.user.id)

        return Response('', 201)


@api.resource('/voice/is-first')
class CheckVoiceRecordIsFirstTime(BaseResource):
    @auth_required(AccountModel)
    def get(self):
        return {
            'isFirst': not bool(g.user.voice_avg)
        }
