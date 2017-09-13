'''A module to test that sms are added by a user'''
from hc.api.models import Channel
from hc.test import BaseTestCase

class AddSmsTestCase(BaseTestCase):
    '''A class that Tests the front end side of adding a number for sms'''
    def login_user(self):
        '''A method that logs in a user alice to reduce repetition'''
        self.client.login(username="alice@example.org", password="password")
    def test_add_number(self):
        '''A method that tests adding a number that is valid, after logging
        in alice as a user. The number in this case is valid and exists as
        confirmed by twilio.
        '''
        url = "/integrations/add/"
        form = {"kind": "sms", "value": "+254722000000"}
        self.login_user()
        post_sms_number = self.client.post(url, form)
        self.assertRedirects(post_sms_number, "/integrations/")
        self.assertEqual(Channel.objects.count(), 1)
        get_integration_page = self.client.get("/integrations/")
        self.assertContains(get_integration_page, "254722000000")
        