from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        assert result, "handle_many should return True"

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        assert set(names) == set(handled_names)
        ## The above assert fails. Make it pass

    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_many()

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_changes_next_nag_after_notification(self, mock):
        check = Check(user=self.alice, status="down")
        check.nag_time = timedelta(minutes=3)
        check.grace = timedelta(minutes=1)
        check.timeout = timedelta(minutes=1)
        now = timezone.now()
        check.next_nag = now
        check.last_ping = now - timedelta(minutes=10)
        check.save()
        Command().handle_many()
        checks = Check.objects.filter(status="down", nag_mode=True).first()
        next_time = now + timedelta(minutes=3)
        assert checks.next_nag >= next_time

    ### Assert when Command's handle many that when handle_many should return True
