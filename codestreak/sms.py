# -*- coding: utf-8 -*-
import os
import random

from twilio.rest import TwilioRestClient

from .email import SUBJECT_LINES


def sms_notify(github_event, reminder):

    text = random.choice(SUBJECT_LINES)

    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    FROM_NUMBER = os.environ['TWILIO_FROM_NUMBER']
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        body=text,
        to=reminder.sms_number,
        from_=FROM_NUMBER
    )