from hc.api.models import Check
from hc.test import BaseTestCase


class UpdatePriorityTestCase(BaseTestCase):

    def setUp(self):
        super(UpdatePriorityTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_priority_changes_to_low_when_high(self):
        """
        Test checks that the priority is updated to Low when previously High
        """
        self._set_priority("High")
        self.assertEqual(self.check.priority, "Low")

    def test_priority_initially_low(self):
        """
        Test checks that the priority is updated to Low when previously High
        """
        self.assertEqual(self.check.priority, "Low")

    def test_priority_change_to_high_when_low(self):
        """
        Test checks that the priority is updated to High when previously Low
        """
        self._set_priority("Low")
        self.assertEqual(self.check.priority, "High")

    def _set_priority(self, priority):
        """
        Sets priority for testing
        """
        self.check.priority = priority
        self.check.save()
        url = "/checks/%s/priority/" % self.check.code

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")

        self.check.refresh_from_db()