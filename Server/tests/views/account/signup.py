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

        self._request = lambda *, token=None, id=self.primary_user.id: self.request(
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
        resp = self._request(id=self.primary_user.id + '!')

        # (2) status code 200
        self.assertEqual(resp.status_code, 200)


class TestInitializeInfo(TCBase):
    """
    기본 정보 업로드를 테스트합니다.
    """
    def __init__(self, *args, **kwargs):
        super(TestInitializeInfo, self).__init__(*args, **kwargs)

        self.method = self.client.post
        self.target_uri = '/initialize/info/{}'

    def setUp(self):
        super(TestInitializeInfo, self).setUp()

        # ---

        self.shortest_cycle = self.primary_user.shortest_cycle
        self.longest_cycle = self.primary_user.longest_cycle
        self.last_mens_start_date = self.primary_user.last_mens_start_date
        self.last_mens_start_date_str = self.last_mens_start_date.strftime('%Y-%m-%d')

        self.primary_user.update(
            shortest_cycle=None,
            longest_cycle=None,
            last_mens_start_date=None
        )

        self._request = lambda *, token=None, id=self.primary_user.id, shortest_cycle=self.shortest_cycle, longest_cycle=self.longest_cycle, last_mens_start_date=self.last_mens_start_date_str: self.request(
            self.method,
            self.target_uri.format(id),
            token,
            json={
                'shortestCycle': shortest_cycle,
                'longestCycle': longest_cycle,
                'lastMensStartDate': last_mens_start_date
            }
        )

    def testInitializeInfoSuccess(self):
        # (1) 기본 정보 업로드
        resp = self._request()

        # (2) status code 201
        self.assertEqual(resp.status_code, 201)

        # (3) 데이터베이스 확인
        self.primary_user.reload()

        self.assertEqual(self.primary_user.shortest_cycle, self.shortest_cycle)
        self.assertEqual(self.primary_user.longest_cycle, self.longest_cycle)
        self.assertEqual(self.primary_user.last_mens_start_date, self.last_mens_start_date)

    def testInitializeInfoWithAlreadyInitializedUser(self):
        # (1) 이미 기본 정보가 업로드된 유저로 업로드
        resp = self._request(id=self.secondary_user.id)

        # (2) status code 201
        self.assertEqual(resp.status_code, 201)

        # (3) 데이터베이스 확인
        self.secondary_user.reload()

        self.assertNotEqual(self.secondary_user.shortest_cycle, self.shortest_cycle)
        self.assertNotEqual(self.secondary_user.longest_cycle, self.longest_cycle)
        self.assertNotEqual(self.secondary_user.last_mens_start_date, self.last_mens_start_date)

    def testInitializeInfoWithDoesNotExistingID(self):
        # (1) 존재하지 않는 ID로 업로드
        resp = self._request(id='123')

        # (2) status code 204
        self.assertEqual(resp.status_code, 204)

    def testInitializeInfoWithShortestCycleIsBiggerThanLongestCycle(self):
        # (1) 가장 짧은 주기가 가장 긴 주기보다 크게
        resp = self._request(shortest_cycle=self.longest_cycle + 1)

        # (2) status code 400
        self.assertEqual(resp.status_code, 400)
