from app.models import *
from app.models.account import AccountModel


class VoiceModel(Document):
    meta = {
        'collection': 'voice'
    }

    owner = ReferenceField(
        document_type=ReferenceField,
        required=True
    )

    filename = StringField(
        required=True
    )


class EmotionModel(Document):
    meta = {
        'collection': 'emotion'
    }


