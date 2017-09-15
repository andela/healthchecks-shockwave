import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json()["error"], expected_error)

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        self.assertIn("ping_url", doc)
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        self.assertEqual(doc['last_ping'], None)
        self.assertEqual(doc['n_pings'], 0)

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})
        resp = self.client.post(self.URL, payload, HTTP_X_API_KEY="abc", 
                content_type="application/json")
        self.assertEqual(resp.status_code, 201)

    def test_it_handles_missing_request_body(self):
        resp = self.client.post(self.URL,content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"], "wrong api_key")

    def test_it_handles_invalid_json(self):
        resp = self.client.post(self.URL, "name is", HTTP_X_API_KEY="abc", 
                content_type="application/json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        resp = self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"], "wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        resp = self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"],"timeout is not a number") 

    def test_it_rejects_non_string_name(self):
        resp = self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"], "name is not a string")


    def test_for_assignment_of_channels(self):
        channel = Channel(user=self.alice)
        channel.save()

        resp = self.post({"api_key" : "abc", "channels" : "*"})
        self.assertEqual(resp.status_code, 201)
        check = Check.objects.get()

        self.assertEqual(check.channel_set.get(), channel)

    def test_timeout_is_too_small(self):
        resp = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 1,
            "grace": 60
        })
        self.assertEqual(resp.json()["error"], "timeout is too small")

    def test_timeout_is_too_large(self):
        resp = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3000000,
            "grace": 60
        })
        self.assertEqual(resp.json()["error"], "timeout is too large")
