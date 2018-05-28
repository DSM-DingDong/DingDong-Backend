from app.models import *


class VoiceModel(Document):
    meta = {
        'collection': 'voice'
    }

    owner = ReferenceField(
        document_type='AccountModel',
        required=True,
        reverse_delete_rule=CASCADE
    )

    filename = StringField(
        required=True
    )


class EmotionModel(Document):
    meta = {
        'collection': 'emotion'
    }


