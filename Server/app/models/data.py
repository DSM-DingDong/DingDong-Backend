from datetime import datetime

from app.models import *


class VoiceModel(Document):
    meta = {
        'collection': 'voice'
    }

    date = StringField(
        default=datetime.now().strftime('%Y-%m-%d')
    )

    owner = ReferenceField(
        document_type='AccountModel',
        required=True,
        reverse_delete_rule=CASCADE
    )

    filename = StringField(
        required=True
    )
