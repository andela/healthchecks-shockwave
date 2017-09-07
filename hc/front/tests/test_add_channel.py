from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_works(self):
        """Test that team members can view all added channels, added by any
        member in the team while non-members cannot.
        Bob a team member adds an email channel. Alice logs in and views email
        channel added on her page. Test that channel added contains the user
        name of the alice who is the team creator.
        """
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
