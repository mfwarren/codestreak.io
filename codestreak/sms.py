# -*- coding: utf-8 -*-
import os
import random

from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException

SUBJECT_LINES = [
    'CodeStreak.io: reminder to commit!',
    'Even source code needs love sometimes',
    '⏰ time to code ⏰',
    '⭐⭐⭐ gold stars if you can push some code',
    '🌠 Keep the streak going!',
    'do some coding then celebrate! 🍺🍺🍻 🎉🎉🎉',
    'keep your perfect score going 💯',
    'get coding! (reminder you can reply with STOP to cancel these messages)',
    "I'm still waiting to see some code from you today",
    "GitHub misses you",
    'Just write something quick',
    '15 minutes of practice coding could level you up',
    "here's a challenge: how many ways do you know to print to stdout",
    "I'm watching your account, waiting to see your next brilliant commit"
]


def sms_notify(github_event, reminder):

    text = random.choice(SUBJECT_LINES)

    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    FROM_NUMBER = os.environ['TWILIO_FROM_NUMBER']
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=text,
            to=reminder.sms_number,
            from_=FROM_NUMBER
        )
    except TwilioRestException as ex:
        print("Failed to send SMS to {}".format(reminder.sms_number))