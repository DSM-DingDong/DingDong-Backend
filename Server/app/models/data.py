from mongoengine import *


class VoiceModel(Document):
    meta = {
        'collection': 'voice'
    }

    date = StringField(
        required=True
    )

    owner = ReferenceField(
        document_type='AccountModel',
        required=True,
        reverse_delete_rule=CASCADE
    )

    filename = StringField(
        required=True,
        unique=True
    )
