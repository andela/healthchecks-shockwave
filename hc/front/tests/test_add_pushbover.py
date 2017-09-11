'''A module that tests adding of pushover notifications by a user'''
from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    '''A class to test adding of a pushover channel, and check that controls
    exist to ascertain valid requests for pushovers.
    '''

    def test_it_adds_channel(self):
        '''Test a pushover channel is added by passing valid credentials.
        A user is logged in. Session is created with valid nonce for
        ascertaining a new session. Priority of normal is passed. User is
        redirected. Channel should contain one object.
        '''
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        get_request = self.client.get("/integrations/add_pushover/?%s" % params)
        assert get_request.status_code == 302

        channels = list(Channel.objects.all())
        assert len(channels) == 1
        assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        '''Test that pushover_api_token is checked if it exists.
        User logs in with no pushover token.
        '''
        self.client.login(username="alice@example.org", password="password")
        r_with_no_token = self.client.get("/integrations/add_pushover/")
        self.assertEqual(r_with_no_token.status_code, 404)

    def test_it_validates_nonce(self):
        '''Test that nonce is validated before a pushover channel is added.
        Lack of nonce forbids the user from access.
        '''
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r_with_invalid_nonce = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r_with_invalid_nonce.status_code == 403

    def test_it_validates_priority(self):
        '''Test parameter priority is checked before adding a pushover.
        Pushover priority parameter should range as:
        -2 -- Lowest priority
        -1 -- Low priority
        0 -- Normal
        1 -- High priority
        2 -- Emergency priority
        Parameter outside above range should return bad request status code.
        '''

        self.client.login(username="alice@example.org", password="password")
        session = self.client.session
        session["po_nonce"] = "n"
        session.save()
        invalid_prio_param_1 = "pushover_user_key=a&nonce=n&prio=-3"
        invalid_prio_param_2 = "pushover_user_key=a&nonce=n&prio=3"
        r_with_invalid_prio = self.client.get("/integrations/add_pushover/?%s"
                                              % invalid_prio_param_1)
        assert r_with_invalid_prio.status_code == 400
        r_with_invalid_prio_2 = self.client.get("/integrations/add_pushover/?%s"
                                                % invalid_prio_param_2)
        self.assertEqual(r_with_invalid_prio_2.status_code, 400)
