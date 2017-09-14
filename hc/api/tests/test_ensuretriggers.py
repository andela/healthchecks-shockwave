from datetime import timedelta

from django.test import TestCase
from unittest import TestCase as TCase
from django.utils import timezone

from hc.api.management.commands.ensuretriggers import Command
from hc.api.models import Check


class EnsureTriggersTestCase(TestCase):

    def test_ensure_triggers(self):
        Command().handle()

        check = Check.objects.create()
        self.assertIsNone(check.alert_after)

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        self.assertIsNotNone(check.alert_after)

        alert_after = check.alert_after

        check.last_ping += timedelta(days=1)
        check.save()
       
        check.refresh_from_db()
        self.assertLess(alert_after, check.alert_after)

    def test_ensure_triggers_alert_before(self):
        """
        Tests that alert before is always reset after every ping
        """
        Command().handle()

        check = Check.objects.create()
        assert check.alert_before is None

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        assert check.alert_before is not None

        alert_before = check.alert_before

        check.last_ping += timedelta(hours=22)
        check.save()
        check.refresh_from_db()
        self.assertGreater(check.alert_before, alert_before)

    def test_alert_before_set_to_expected_time(self):
        """
        Tests that alert before is set to the expected time which would be an addition
        of the time of last_ping and timeout and the total subtracted by the grace period
        """
        Command().handle()

        check = Check.objects.create()
        assert check.alert_before is None

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        self.assertEqual(check.alert_before, (check.last_ping+check.timeout-check.grace))

