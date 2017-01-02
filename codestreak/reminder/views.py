# -*- coding: utf-8 -*-
"""User views."""
from functools import wraps

from flask import Blueprint, render_template, redirect, session, url_for

from codestreak.reminder.models import Reminder
from codestreak.reminder.forms import EditReminder

blueprint = Blueprint('reminder', __name__, url_prefix='/reminders', static_folder='../static')


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


@blueprint.route('/', methods=['GET', 'POST'])
@requires_auth
def settings():
    """Edit settings."""
    reminder = Reminder.for_username(session['profile']['nickname'])
    form = EditReminder(obj=reminder)
    if form.validate_on_submit():
        form.populate_obj(reminder)
        reminder.save()
        return redirect(url_for('reminder.settings'))
    return render_template('reminders/settings.html', form=form)
