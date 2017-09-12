from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        """Create a new user, and assert setup email was sent"""
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        response = self.client.post("/accounts/login/", form)
        self.assertEqual(response.status_code, 302)

        ### Assert that a user was created
        user = User.objects.filter(email="alice@example.org").first()
        self.assertTrue(user)

        # And email sent
        self.assertEqual(len(mail.outbox), 1)

        ### Assert contents of the email body
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        
        ### Assert that check is associated with the new user
        check = Check.objects.filter(user=user.id).first()
        self.assertTrue(check)

    def test_it_pops_bad_link_from_session(self):
        """ Sets a bad_link session variable and verifies that logging in
        removes it """
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

    def test_renders_login_page(self):
        """ Tests that the login page is returned on a get request """
        response = self.client.get("/accounts/login/")
        self.assertContains(response, "Please enter your email address.")

    def test_redirects_new_user(self):
        """ Tests redirection to login link sent page for new user """
        response = self.client.post("/accounts/login/",
                                    {"email": "test@test.com"})
        self.assertRedirects(response, "/accounts/login_link_sent/")

    def test_redirects_valid_to_checks(self):
        """ Tests redirects to checks for valid credentials """
        user = User(username="robert", email="robert@example.org")
        user.set_password("roba")
        user.save()

        form = {"email": "robert@example.org", "password": "roba"}
        response = self.client.post("/accounts/login/", form)
        self.assertRedirects(response, "/checks/")

    def test_invalid_credentials(self):
        """ Check if it redirects to login page for invalid credentials """
        response = self.client.post("/accounts/login/",
                                    {"email": "test@test.com",
                                     "password": "pass"})
        self.assertContains(response, "Incorrect email or password.")

