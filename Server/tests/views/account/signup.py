from tests.views import TCBase


class TestIDCheck(TCBase):
    """
    자체 계정의 ID 중복체크를 테스트합니다.
    """
    def __init__(self, *args, **kwargs):
        super(TestIDCheck, self).__init__(*args, **kwargs)

        self.method = self.client.get
        self.target_uri = '/check/id/{}'

    def setUp(self):
        super(TestIDCheck, self).setUp()

        # ---

        self._request = lambda *, token=None, id=self.primary_user_id: self.request(
            self.method,
            self.target_uri.format(id),
            token,
        )

    def testDuplicatedID(self):
        # (1) 이미 가입된 ID로 중복체크
        resp = self._request()

        # (2) status code 409
        self.assertEqual(resp.status_code, 409)

    def testNotDuplicatedID(self):
        # (1) 가입되지 않은 ID로 중복체크
        resp = self._request(id=self.primary_user_id + '!')

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)
