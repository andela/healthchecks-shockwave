from hc.test import BaseTestCase
from hc.api.models import Check
from django.contrib.auth.models import User
from hc.accounts.models import Profile

class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)

        ### Assert the contents of r


    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url)
        ### Assert the expected error code

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        ### Assert the expected error code
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)

    def test_it_views_assigned_checks_only(self):
        self.tony = User(username="tony", email="tony@yes.com")
        self.tony.set_password("1111")
        self.tony.save()
        self.profile = Profile(user=self.tony)
        self.profile.save()
        self.client.login(username="alice@example.org", password="password")
        url = "/checks/add/"
        url2 = "/checks/"
        r = self.client.post(url)
        check = Check.objects.get(status="new")
        check_ping = str(check.code)
        check_ping2 = "aaaaaaa" + check_ping

        r = self.client.post("/accounts/profile/",
                             data={"invite_team_member": "1",
                                   "email": "tony@yes.com",
                                   "check-1": check_ping2})
        self.assertContains(r, "Invitation to tony@yes.com sent")
        self.client.logout()
        self.client.login(username="tony@yes.com", password="1111")
        def_page = self.client.get(url2)
        self.assertContains(def_page, "alice@example.org")
