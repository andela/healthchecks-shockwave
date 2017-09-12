from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check
from mock import patch


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
        ### Repeat above test for when check is an empty string

    def test_status_works_with_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)

        self.assertTrue(check.in_grace_period())
        self.assertEqual(check.get_status(), "up")

        ### The above 2 asserts fail. Make them pass

    def test_paused_check_is_not_in_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    ### Test that when a new check is created, it is not in the grace period

    def test_update_status_often_to_up(self):
        """
        Test that get_status updates status often to up when duration since the last
        ping exceeds the time set at reverse grace period
        """
        check = Check()

        check.status = "often"
        check.last_ping = timezone.now() - timedelta(hours=23, minutes=1)
        self.assertEqual(check.get_status(), "up")

    def test_ping_often_returns_status_often(self):
        """
        Test to check that if a ping is sent with in before the reverse grace period
        the  method ping_often returns status often and sends an alert
        """
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(hours=22, minutes=30)
        check.save()
        self.assertEqual(check.ping_often(), "often")

    def test_ping_often_returns_status_up(self):
        """
        Test that a ping sent with in and after reverse grace period would return
        up
        """
        check = Check()
        check.status = "often"

        check.last_ping = timezone.now() - timedelta(hours=23, minutes=30)
        self.assertEqual(check.ping_often(), "up")

    def test_ping_often_returns_original_status(self):
        """
        Test to check that if a ping is sent with status new or paused then that same status
        is returned
        """
        check = Check()
        check.status = "new"

        self.assertEqual(check.ping_often(), "new")
