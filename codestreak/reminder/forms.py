# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import BooleanField, StringField
from wtforms.validators import ValidationError

from twilio.rest.lookups import TwilioLookupsClient


class EditReminder(Form):
    """Reminder form."""

    enabled = BooleanField('Enabled')
    email_enabled = BooleanField('Notify By Email Enabled')
    sms_enabled = BooleanField('Notify By SMS Enabled')
    sms_number = StringField('Mobile phone number')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EditReminder, self).__init__(*args, **kwargs)

    def validate_sms_number(self, field):
        try:
            client = TwilioLookupsClient()
            match = client.phone_numbers.get(field.data)
            field.data = match.phone_number
        except Exception as ex:
            print(ex)
            raise ValidationError('Failed to validate this phone number')
