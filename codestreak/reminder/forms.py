# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import BooleanField, StringField


class EditReminder(Form):
    """Reminder form."""

    enabled = BooleanField('Enabled')
    email_enabled = BooleanField('Notify By Email Enabled')
    sms_enabled = BooleanField('Notify By SMS Enabled')
    sms_number = StringField('Mobile phone number')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EditReminder, self).__init__(*args, **kwargs)
