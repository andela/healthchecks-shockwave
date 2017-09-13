'''A module to test the sms file for sending sms.
'''
from hc.test import BaseTestCase
from hc.lib.send_sms import TwilioSendSms
from django.test.utils import override_settings
from django.core.exceptions import MiddlewareNotUsed

class TestTilioSendSms(BaseTestCase):
    '''A class that tests validation of a number and the loading of
    configured values for the server's twilio account.
    '''
    def test_valid_number(self):
        '''A method that passes a list of valid numbers and asserts that
        they are confirmed to be valid, while also passes invalid numbers
        and asserts that they are invalid.
        '''
        valid_numbers = ["+254718217411", "+14157012311", "+270860123000"]
        for number in valid_numbers:
            self.assertEqual(TwilioSendSms().check_number(number), True)
        invalid_numbers = ["+2547182174", "+141570311", "+270863000"]
        for number in invalid_numbers:
            self.assertEqual(TwilioSendSms().check_number(number), False)
            