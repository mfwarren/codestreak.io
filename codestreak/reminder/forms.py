# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import BooleanField


class EditReminder(Form):
    """Reminder form."""

    enabled = BooleanField('Enabled')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EditReminder, self).__init__(*args, **kwargs)
