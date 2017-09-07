from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_access(self):
        """Test that team members can view all added checks, added by any
        member in the team while non-members cannot.
        Alice the team lead adds a check. Bob a team member of Alice's team
        opens his page and views a check Alice added on his page. Charlie a
        non-team member opens his page and does not have a view of a check.
        """
        url1 = "/checks/add/"
        url2 = "/checks/"
        self.client.login(username="alice@example.org", password="password")
        post_check_alice = self.client.post(url1)
        self.assertRedirects(post_check_alice, "/checks/")
        self.client.logout()
        value = Check.objects.all()
        alices_check = list(value)[0]
        self.client.login(username="bob@example.org", password="password")
        bobs_checks = self.client.get(url2)
        self.assertContains(bobs_checks, alices_check.code)
        self.client.logout()
        self.client.login(username="charlie@example.org", password="password")
        charlies_checks = self.client.get(url2)
        self.assertNotContains(charlies_checks, alices_check.code)
