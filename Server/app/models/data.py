from app.models import *


class VoiceModel(Document):
    meta = {
        'collection': 'voice'
    }

    owner = ReferenceField(
        document_type='AccountModel',
        required=True
    )

    filename = StringField(
        required=True
    )


class EmotionModel(Document):
    meta = {
        'collection': 'emotion'
    }


