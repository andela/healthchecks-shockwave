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

    def test_invalid_number_entries(self):
        '''A method that tests that passing invalid data to the form for the sms
        will not lead to creation of a channel. Arguments to be rejected are
        strings -- the form should accept only numbers.
        '''
        url = "/integrations/add/"
        form_list = [{"kind": "sms", "value": "uiouio"}, {"kind": "sms", "value": "1234"}]
        self.login_user()
        for form in form_list:
            post_sms_number = self.client.post(url, form)
            self.assertNotEqual(post_sms_number.status_code, 302)
            self.assertEqual(Channel.objects.count(), 0)
