# -*- coding: utf-8 -*-
import os
import random

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

# Email Infrastructure
# --------------------

API_KEY = os.environ['SENDGRID_API_KEY']
sg = sendgrid.SendGridAPIClient(apikey=API_KEY)

TEMPLATE = """{}









=========

A friendly nudge brought to you by CodeStreak.io.

A Matt Warren (mattwarren.co) project.



"""

SUBJECT_LINES = [
    'CodeStreak.io: reminder to commit!',
    'Even source code needs love sometimes',
    '⏰ time to code ⏰',
    '⭐⭐⭐ gold stars if you can push some code',
    '🌠 Keep the streak going!',
    'do some coding then celebrate! 🍺🍺🍻 🎉🎉🎉',
    'keep your perfect score going 💯',
    'coding idea: What could you automate?',
    'how about coding hello world in a new language?',
    'are there any libraries you are curious to try out?'
]


def notify(note, email_address):

    subject = random.choice(SUBJECT_LINES)
    message = TEMPLATE.format(note)

    from_address = Email('no-reply@codestreak.io', name="CodeStreak.io")
    to_address = Email(email_address)
    content = Content('text/plain', message)

    mail = Mail(from_address, subject, to_address, content)
    sg.client.mail.send.post(request_body=mail.get())
