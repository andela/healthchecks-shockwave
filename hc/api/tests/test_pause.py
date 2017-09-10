from hc.api.models import Check
from hc.test import BaseTestCase


class PauseTestCase(BaseTestCase):

    def test_it_works(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")
        assert r.status_code == 200

    def test_it_validates_ownership(self):
        check = Check(user=self.bob, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        r = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(r.status_code, 400)

    def test_that_it_only_allows_post_requests(self):
        check = Check(user=self.alice, status="up")
        check.save()

        url = "/api/v1/checks/%s/pause" % check.code
        resp = self.client.get(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        assert resp.status_code == 405

    def test_it_validates_uuid(self):
        url = "/api/v1/checks/07c2f548-9850-4b27-af5d-6c9dc157ec03/pause"
        resp = self.client.post(url, "", content_type="application/json",
                             HTTP_X_API_KEY="abc")

        self.assertEqual(resp.status_code, 400)
