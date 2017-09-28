from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        r = self._uniform_pause_test_case(self.alice, 'post')
        self.assertEqual(r.status_code, 200)

    def test_it_validates_ownership(self):
        r = self._uniform_pause_test_case(self.bob, 'post')
        self.assertEqual(r.status_code, 400)

    def test_that_it_only_allows_post_requests(self):
        resp = self._uniform_pause_test_case(self.alice, 'get')
        self.assertEqual(resp.status_code, 405)

    def test_it_validates_uuid(self):
        url = "/api/v1/checks/07c2f548-9850-4b27-af5d-6c9dc157ec03/pause"
        resp = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")
        self.assertEqual(resp.status_code, 400)

    def _uniform_pause_test_case(self, user, request):
        check = Check(user=user, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        if request is 'get':
            return self.client.get(url, "", content_type="application/json", HTTP_X_API_KEY="abc")
        return self.client.post(url, "", content_type="application/json", HTTP_X_API_KEY="abc")
