from django.core import mail
from hc.test import BaseTestCase
from hc.accounts.models import Member, Profile, User
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        """ Asserts a set password email is sent during account set up """
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        response = self.client.post("/accounts/profile/", form)
        assert response.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        
        ### Assert that the token is set
        self.assertTrue(token, "Token should be set")

        ### Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)

        ### Assert contents of the email body
        self.assertIn('Set password on healthchecks.io', mail.outbox[0].subject)

    def test_it_sends_report(self):
        """assert contents of report email sent"""
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        ###Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)

        ### Assert contents of the email body
        self.assertEqual(mail.outbox[0].subject, "Monthly Report")

    def test_it_adds_team_member(self):
        """test adding member to a team, and invitation email assertion"""
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 200)

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        ### Assert the existence of the member emails
        self.assertTrue("frank@example.org" in member_emails)

        ###Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)

        ### Assert contents of the email body
        self.assertEqual(mail.outbox[0].subject, "You have been invited to join alice@example.org on healthchecks.io")

    def test_add_team_member_checks_team_access_allowed_flag(self):
        """ Logs in a user whose profile by default doesn't allow team
        access, tests adding another user to a team, which returns
        HTTP forbidden code 403 """
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 403)

    def test_it_removes_team_member(self):
        """remove a member from a team, and assert s/he is no longer a member"""
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        response = self.client.post("/accounts/profile/", form)
        assert response.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        """set new team name for alice's team, and
        assert the new name is set"""
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 200)

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")
        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        response = self.client.post("/accounts/profile/", form)
        self.assertEqual(response.status_code, 403)

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")
        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        response = self.client.get("/accounts/profile/")
        self.assertContains(response, "foo.svg")
        self.assertContains(response, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(response, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(response, "bobs-tag.svg")

    def test_creates_and_revokes_api_key(self):
        """Test it creates and revokes API key"""
        #create a new user
        user = User(username="robert", email="robert@example.org")
        user.set_password("roba")
        user.save()
        form = {"email": "robert@example.org", "password": "roba"}
        self.client.post("/accounts/login/", form)

        #create an api key for the new user, and assert it has been created.
        self.client.post("/accounts/profile/", {"create_api_key": '1'})
        api_key = User.objects.get(email='robert@example.org').profile.api_key
        self.assertTrue(api_key)

        #Create an api key for the new user, revoke it and assert the key is not existent.
        self.client.post("/accounts/profile/", {"create_api_key": '1'})
        self.client.post("/accounts/profile/", {"revoke_api_key": '1'})
        api_key = User.objects.get(email='robert@example.org').profile.api_key
        self.assertFalse(api_key)
        