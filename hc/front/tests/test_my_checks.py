from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            response = self.client.get("/checks/")
            self.assertContains(response, "Alice Was Here", status_code=200)

    def test_it_shows_green_check(self):
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/checks/")

        # Desktop
        self.assertContains(response, "icon-up")

        # Mobile
        self.assertContains(response, "label-success")

    def test_it_shows_red_check(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/checks/")
        self.assertContains(response, "icon-nag")
        self.assertContains(response, "icon-down")
        # Mobile
        self.assertContains(response, "label-danger")

    def test_it_shows_amber_check(self):
        self.check.last_ping = timezone.now() - td(days=1, minutes=30)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/checks/")

        # Desktop
        self.assertContains(response, "icon-grace")

        # Mobile
        self.assertContains(response, "label-warning")

    def test_failed_checks_view(self):
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/checks/failed/")

        # Desktop
        self.assertNotContains(response, "icon-up")
        self.assertNotContains(response, "icon-grace")
        self.assertContains(response, "icon-down")

        # Mobile
        self.assertNotContains(response, "label-warning")
        self.assertNotContains(response, "label-success")
        self.assertContains(response, "label-danger")
