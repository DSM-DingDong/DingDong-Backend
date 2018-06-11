from uuid import uuid4

import jwt

from flask_jwt_extended import create_refresh_token

from app.models.account import AccountModel, AccessTokenModel, RefreshTokenModel

from tests.views import TCBase


class TestAuth(TCBase):
    """
    자체 계정 로그인을 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestAuth, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/auth/common'

    def setUp(self):
        super(TestAuth, self).setUp()

        # ---

        self._request = lambda *, token=None, id=self.primary_user.id, pw=self.primary_user_pw: self.request(
            self.method,
            self.target_uri,
            token,
            json={
                'id': id,
                'pw': pw
            }
        )

    def testAuthSuccess(self):
        # (1) 로그인
        resp = self._request()

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        data = resp.json

        self.assertIn('accessToken', data)
        self.assertIn('refreshToken', data)

        access_token = data['accessToken']
        refresh_token = data['refreshToken']

        self.assertIsInstance(access_token, str)
        self.assertIsInstance(refresh_token, str)

        self.assertRegex(data['accessToken'], self.token_regex)
        self.assertRegex(data['refreshToken'], self.token_regex)

        # (4) 데이터베이스 확인
        access_token_obj = AccessTokenModel.objects(owner=self.primary_user).first()
        self.assertTrue(access_token_obj)
        self.assertEqual(jwt.decode(access_token, self.app.secret_key, 'HS256')['identity'], str(access_token_obj.identity))

        refresh_token_obj = RefreshTokenModel.objects(owner=self.primary_user).first()
        self.assertTrue(access_token_obj)
        self.assertEqual(jwt.decode(refresh_token, self.app.secret_key, 'HS256')['identity'], str(refresh_token_obj.identity))

    def testAuthFailure_incorrectID(self):
        # (1) 존재하지 않는 ID로 로그인
        resp = self._request(id=self.primary_user.id + '1')

        # (2) status code 401
        self.assertEqual(resp.status_code, 401)

    def testAuthFailure_incorrectPW(self):
        # (1) 틀린 PW로 로그인
        resp = self._request(pw=self.primary_user_pw + '1')

        # (2) status code 401
        self.assertEqual(resp.status_code, 401)


class TestFacebookAuth(TCBase):
    """
    페이스북 계정 로그인을 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestFacebookAuth, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/auth/facebook'
        self.fb_id = '100006735372513'

    def setUp(self):
        super(TestFacebookAuth, self).setUp()

        # ---

        self._request = lambda *, token=None, fb_id=self.fb_id: self.request(
            self.method,
            self.target_uri,
            token,
            json={
                'fbId': fb_id
            }
        )

    def testAuthSuccessWithSignup(self):
        # (1) 로그인
        resp = self._request()

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        data = resp.json

        self.assertIn('accessToken', data)
        self.assertIn('refreshToken', data)

        access_token = data['accessToken']
        refresh_token = data['refreshToken']

        self.assertIsInstance(access_token, str)
        self.assertIsInstance(refresh_token, str)

        self.assertRegex(data['accessToken'], self.token_regex)
        self.assertRegex(data['refreshToken'], self.token_regex)

        # (4) 데이터베이스 확인
        user = AccountModel.objects(id=self.fb_id).first()

        access_token_obj = AccessTokenModel.objects(owner=user).first()
        self.assertTrue(access_token_obj)
        self.assertEqual(jwt.decode(access_token, self.app.secret_key, 'HS256')['identity'], str(access_token_obj.identity))

        refresh_token_obj = RefreshTokenModel.objects(owner=user).first()
        self.assertTrue(refresh_token_obj)
        self.assertEqual(jwt.decode(refresh_token, self.app.secret_key, 'HS256')['identity'], str(refresh_token_obj.identity))

    def testAuthFailure_invalidFbId(self):
        # (1) 존재하지 않는 ID로 로그인
        resp = self._request(fb_id=self.fb_id + '12345')

        # (2) status code 401
        self.assertEqual(resp.status_code, 401)


class TestRefresh(TCBase):
    """
    JWT 토큰 refresh를 테스트합니다.
    """

    def __init__(self, *args, **kwargs):
        super(TestRefresh, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/refresh'

    def setUp(self):
        super(TestRefresh, self).setUp()

        # ---

        self._request = lambda *, token=None: self.request(
            self.method,
            self.target_uri,
            token
        )

    def testRefreshSuccess(self):
        # (1) refresh
        resp = self._request(token=self.primary_user_refresh_token)

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)

        # (3) response data
        data = resp.json

        self.assertIn('accessToken', data)

        access_token = data['accessToken']

        self.assertIsInstance(access_token, str)

        self.assertRegex(data['accessToken'], self.token_regex)

        # (4) 데이터베이스 확인
        access_token_obj = AccessTokenModel.objects(owner=self.primary_user).first()
        self.assertTrue(access_token_obj)
        self.assertEqual(jwt.decode(access_token, self.app.secret_key, 'HS256')['identity'], str(access_token_obj.identity))

    def testRefreshFailure_invalidToken(self):
        # (1) 유효하지 않은 refresh token을 통해 refresh
        with self.app.app_context():
            resp = self._request(token='JWT {}'.format(create_refresh_token(str(uuid4()))))

        # (2) status code 401
        self.assertEqual(resp.status_code, 401)

    def testRefreshFailure_invalidIdentityFormat(self):
        # (1) 유효하지 않은 identity 값이 들어간 refresh token을 통해 refresh
        with self.app.app_context():
            resp = self._request(token='JWT {}'.format(create_refresh_token('123')))

        # (2) status code 422
        self.assertEqual(resp.status_code, 422)
