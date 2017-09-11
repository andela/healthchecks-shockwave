from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


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

    def test_check_before_reverse_grace_period(self):
        """
        Test to check that if a ping is sent with in the reverse grace period
        the  method before_reverse_grace_period returns true
        """
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(hours=22, minutes=30)
        self.assertTrue(check.before_reverse_grace_period())

    def test_check_in_return_grace_period_returns_false(self):
        """
        Test that if check is pinged in the time allocation of reverse grace period
        the method before_reverse_grace_period returns false
        """
        check = Check()
        check.status = "up"

        check.last_ping = timezone.now() - timedelta(hours=23, minutes=30)
        self.assertFalse(check.before_reverse_grace_period())
