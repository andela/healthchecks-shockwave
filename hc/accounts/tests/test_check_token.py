from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        """set a token for alice's profile"""
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_redirects(self):
        """Login and assert it redirects to the checks page"""
        response = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_login_redirects(self):
        """Login and test it redirects already logged in"""
        self.client.post("/accounts/check_token/alice/secret-token/")
        response = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

    def test_login_badtoken(self):
        """Login with a bad token and check that it redirects"""
        response = self.client.post("/accounts/check_token/alice/wrong_token/")
        self.assertRedirects(response, "/accounts/login/")

    def test_redirects_wrong_username(self):
        """Test it redirects to login page, when using non-existent username"""
        response = self.client.post("/accounts/check_token/obama/wrong_token/")
        self.assertRedirects(response, "/accounts/login/")
