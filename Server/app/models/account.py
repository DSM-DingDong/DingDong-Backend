from datetime import datetime
from uuid import uuid4

from app.models import *


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    signup_time = DateTimeField(
        required=True,
        default=datetime.now()
    )

    id = StringField(
        primary_key=True
    )

    pw = StringField()

    shortest_cycle = IntField()
    longest_cycle = IntField()
    # 최근 6개월 간 가장 짧은 주기와 가장 긴 주기

    last_mens_start_date = DateTimeField()
    # 가장 최근 월경시장일

    calendar = DictField(default={})
    # 안전일: 1
    # 가임일: 2
    # 월경시작일: 3
    # 월경중: 4
    # 월경종료일: 5
    calendar_last_modified_time = DateTimeField()
    # calendar 필드가 마지막으로 바뀐 시간


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type='AccountModel',
        primary_key=True,
        reverse_delete_rule=CASCADE
    )

    identity = UUIDField(
        required=True,
        unique=True
    )

    @classmethod
    def generate_token(cls, model, owner):
        while True:
            uuid = uuid4()

            if not model.objects(identity=uuid):
                params = {
                    'owner': owner,
                    'identity': uuid
                }

                if isinstance(model, RefreshTokenModel):
                    params['pw_snapshot'] = owner.pw

                model(**params).save()

                return str(uuid)


class AccessTokenModel(TokenModel):
    meta = {
        'collection': 'access_token'
    }


class RefreshTokenModel(TokenModel):
    meta = {
        'collection': 'refresh_token'
    }

    pw_snapshot = StringField()
