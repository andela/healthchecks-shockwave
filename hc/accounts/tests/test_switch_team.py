from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()
        self.client.login(username="bob@example.org", password="password")
        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)


    def test_it_checks_team_membership(self):
        """test switching to a team one is not a member
        returns forbidden"""
        self.client.login(username="charlie@example.org", password="password")
        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_it_switches_to_own_team(self):
        """test switching to own team, and assert it redirects accordingly"""
        self.client.login(username="alice@example.org", password="password")
        url = "/accounts/switch_team/%s/" % self.alice.username
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)
        
