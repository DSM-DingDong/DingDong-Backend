from app.models import *


class AccountModel(Document):
    meta = {
        'collection': 'account',
    }

    id = StringField(
        primary_key=True
    )

    pw = StringField()
    connected_sns = StringField()


class RefreshTokenModel(Document):
    meta = {
        'collection': 'refresh_token'
    }

    token = UUIDField(
        primary_key=True
    )

    pw_snapshot = StringField()

    owner = ReferenceField(
        document_type=AccountModel,
        required=True
    )
