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
    # 최근 6개월 간 가장 짧은 주기와 가장 긴 주기

    latest_mens_start_date = DateTimeField()
    # 가장 최근 월경시장일

    calendar = DictField(required=True, default={})
    # 안전일: 1
    # 가임일: 2
    # 월경시작일: 3
    # 월경중: 4
    # 월경종료일: 5
    calendar_last_modified_time = DateTimeField()
    # calendar 필드가 마지막으로 바뀐 시간


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


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type='AccountBase',
        primary_key=True
    )

    identity = UUIDField(
        required=True,
        unique=True
    )


class AccessTokenModel(TokenModel):
    meta = {
        'collection': 'access_token'
    }


class RefreshTokenModel(TokenModel):
    meta = {
        'collection': 'refresh_token'
    }

    pw_snapshot = StringField()
