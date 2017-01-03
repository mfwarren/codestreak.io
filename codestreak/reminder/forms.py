# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
import pytz
from wtforms import BooleanField, StringField, SelectField
from wtforms.validators import ValidationError

from twilio.rest.lookups import TwilioLookupsClient


class EditReminder(Form):
    """Reminder form."""

    enabled = BooleanField('Enabled')
    email_enabled = BooleanField('Notify By Email Enabled')
    sms_enabled = BooleanField('Notify By SMS Enabled')
    sms_number = StringField('Mobile phone number')
    timezone = SelectField('Timezone', choices=[(tz,tz) for tz in pytz.common_timezones])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EditReminder, self).__init__(*args, **kwargs)

    def validate_timezone(self, field):
        if field.data not in pytz.common_timezones:
            raise ValidationError('Not a valid timezone')

    def validate_sms_number(self, field):
        if field.data != '' and field.data is not None:
            try:
                client = TwilioLookupsClient()
                match = client.phone_numbers.get(field.data)
                field.data = match.phone_number
            except Exception as ex:
                print(ex)
                raise ValidationError('Failed to validate this phone number')
