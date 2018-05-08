from datetime import datetime

from app.models import *


class AccountBase(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    signup_time = DateTimeField(
        required=True,
        default=datetime.now()
    )

    id = StringField(
        primary_key=True
    )

    shortest_cycle = IntField()
    longest_cycle = IntField()
    latest_mens_start_date = DateTimeField()

    predicted_next_mens_start_date = DateTimeField()


class SystemAccountModel(AccountBase):
    meta = {
        'collection': 'system_account'
    }

    pw = StringField()


class FacebookAccountModel(AccountBase):
    meta = {
        'collection': 'facebook_account'
    }

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
        document_type=AccountBase,
        required=True
    )
