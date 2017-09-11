'''A module to test adding of channels.'''
from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase

@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):
    '''Class to test addition of channels, controls on valid entry of channels
    and proper access by teams on shared channels
    '''

    def test_it_adds_email(self):
        '''Test that a channel email is added.
        Email integration is added with a value for the email. The
        request should redirect to views for integration.
        '''
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        post_email_channel = self.client.post(url, form)

        self.assertRedirects(post_email_channel, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        '''Leading and trailing whitespace should get trimmed.'''

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        '''Test that instructions for each channel integration work while adding'''
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_works(self):
        '''Test that team members can view all added channels, added by any
        member in the team while non-members cannot.
        Bob a team member adds an email channel. Alice logs in and views email
        channel added on her page. Test that channel added contains the user
        name of the alice who is the team creator.
        '''
        url = "/integrations/add/"
        form = {"kind": "email", "value": "team_email@example.org"}
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, form)
        self.client.logout()
        url2 = "/integrations/"
        self.client.login(username="alice@example.org", password="password")
        get_alices_integrations = self.client.get(url2)
        self.assertContains(get_alices_integrations, "team_email@example.org")
        get_added_channel = Channel.objects.get(value="team_email@example.org")
        self.assertEqual(get_added_channel.user.username, 'alice')

    ### Test that bad kinds don't work
    def test_bad_kind_doesnt_work(self):
        '''Test that bad kinds of channels cannot be added
        A bad kind of channel, a channel that does not exist on the tuple
        CHANNEL_KINDS on the api/models.py file, is passed and should return
        a bad request response.
        '''
        url = "/integrations/add/"
        form = {"kind": "gitter", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        post_bad_channel = self.client.post(url, form)
        self.assertEqual(post_bad_channel.status_code, 400)

    def test_interference_across_teams(self):
        '''Test that team creator cannot access non-team members channels.
        Charlie adds a channel and does not belong to any team. Alice owns a
        team but cannot acces channels that belong to Charlie. Charlies added
        channel also stores the user as charlie creating no conflict on non-
        team members.
        '''
        url = "/integrations/add/"
        form = {"kind": "email", "value": "team_email_2@example.org"}
        self.client.login(username="charlie@example.org", password="password")
        self.client.post(url, form)
        self.client.logout()
        url2 = "/integrations/"
        self.client.login(username="alice@example.org", password="password")
        get_alices_integrations = self.client.get(url2)
        self.assertNotContains(get_alices_integrations, "team_email_2@example.org")
        get_charlies_channel = Channel.objects.get(value="team_email_2@example.org")
        self.assertEqual(get_charlies_channel.user.username, 'charlie')
