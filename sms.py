'''A module that sends SMS to users when a change on a status of a check occurs.

Classes:
    TwilioSendSms -- A class that initialises a Twilio client, validates numbers
    and sends messages to users of the app
Functions:
    __init__ -- a method that initialises a twilio client and their server number
    send -- A method for sending messages to a user
    check_number -- A method to assert that a number entered is a valid number
    that exists
    load_config -- A method that returns the configurations for the server on
    their twilio account from their environment variables
'''
import logging
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed

LOGGER = logging.getLogger(__name__)

WRONG_CONFIGURATIONS = """Cannot initialize Twilio notification
middleware. Required enviromental variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""

class TwilioSendSms():
    '''Initialise a Twilio Client based on server number for the product owner's twilio account
    information. Send a message based on the check's status. Validate if a phone number is valid
    '''
    def __init__(self):
        '''Load cofigurations for the user's twilio account as exported while setting up the
        app. Initialise ther server's number and the twilio client with their valid infomation.
        '''
        (twilio_account_sid, twilio_auth_token, twilio_number ) = self.load_config()
        self.twilio_server_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

    def send(self, user_phone_number, message):
        '''Create twilio client object based on initialisation. Call the method /'messagescreate/'
        to send message
        Key word arguments:
        message -- The message to be sent to the user,
        to -- The number of the user of healthchecks.io to whom the message is to be sent to.
        from -- Use the number of the product owner,
        '''
        message = self.twilio_client.messages.create(body=message,
                                                     to=user_phone_number,
                                                     from_=self.twilio_server_number)

    @staticmethod
    def load_config():
        '''A method to load the product owner's twilio account information'''
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN,
                    settings.TWILIO_NUMBER]):
            LOGGER.error(WRONG_CONFIGURATIONS)
            raise MiddlewareNotUsed

        return (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_NUMBER)
