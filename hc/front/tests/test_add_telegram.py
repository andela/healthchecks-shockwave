'''A module to test addition of a telegram user'''
from hc.test import BaseTestCase
from hc.api.models import Channel

class TelegramTestCase(BaseTestCase):
    '''A class to test that a telegram can be added, and that spam telegram users
    cannot be added
    '''
    def test_add_telegram(self):
        '''A method that tests adding a telegam account that is valid, after logging
        in alice as a user.
        '''
        url = "/integrations/add/"
        form = {"kind": "telegram", "first_name": "Crispus", "last_name": "Kamau"}
        self.client.login(username="alice@example.org", password="password")
        post_telegram_user_name = self.client.post(url, form)
        self.assertRedirects(post_telegram_user_name, "/integrations/")
        self.assertEqual(Channel.objects.count(), 1)
        self.assertContains(self.client.get("/integrations/"), "Crispus")

    def test_telegram_user_check(self):
        '''A method that tests that passing invalid users to the form for the telegram
        will not lead to creation of a channel. If no communication has been made
        to the healthchecks bot then the first and last name will not exist, leading to
        lack of creation of a channel
        '''
        url = "/integrations/add/"
        invalid_form_list = [{"kind": "telegram",
                              "first_name": "wrongdata",
                              "last_name": "wrongdata"},
                             {"kind": "telegram",
                              "first_name": "other",
                              "last_name": "other2"}]
        self.client.login(username="bob@example.org", password="password")
        for form in invalid_form_list:
            post_telegram = self.client.post(url, form)
            self.assertNotEqual(post_telegram.status_code, 302)
            self.assertEqual(Channel.objects.count(), 0)
