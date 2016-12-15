import os

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


def notify(note, email_address):

    subject = 'codestreak.io: reminder to commit!'
    message = TEMPLATE.format(note)

    from_address = Email('no-reply@codestreak.io', name="CodeStreak.io")
    to_address = Email(email_address)
    content = Content('text/plain', message)

    mail = Mail(from_address, subject, to_address, content)
    sg.client.mail.send.post(request_body=mail.get())
