# -*- coding: utf-8 -*-
"""User views."""
import os
from collections import Counter
import datetime
from functools import wraps

from flask import Blueprint, render_template, redirect, session, url_for, request
from github import Github
from pytz import timezone
import twilio.twiml

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


@blueprint.route('/sms', methods=['GET', 'POST'])
def twilio_incoming_sms():
    message = request.values.get('Body', '').upper().strip()
    from_number = request.values.get('From', None)
    reminder = Reminder.query.filter_by(sms_number=from_number).first()

    resp = twilio.twiml.Response()

    if message in ['STOP', 'STOPALL', 'UNSUBSCRIBE', 'CANCEL', 'END', 'QUIT']:
        if reminder:
            reminder.sms_enabled = False
            reminder.save()
            resp.message("OK, you will stop recieving these notifications")
        else:
            resp.message("Could not find this phone number registered, login to https://codestreak.io to modify your preferences.")

    elif message in ['UNSTOP', 'START']:
        if reminder:
            reminder.sms_enabled = True
            reminder.save()
            resp.message("OK, your SMS notifications are re-enabled")
        else:
            resp.message("Could not find this phone number registered, login to https://codestreak.io to modify your preferences.")

    elif message in ['HELP', 'INFO']:
        resp.message("https://CodeStreak.io. Daily coding challenge. Reply 'STOP' to cancel notifications")

    else:
        resp.message("Sorry, I'm not programmed to respond")

    return str(resp)


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

    hub = Github(os.getenv('GITHUB_API_TOKEN'))
    hub_user = hub.get_user(reminder.slug)

    events = hub_user.get_public_events()

    # calculate the streak
    base = datetime.datetime.today()
    date_list = [(base - datetime.timedelta(days=x)).date() for x in range(0, 365)]
    histogram = Counter()
    {(base - datetime.timedelta(days=x)).date(): 0 for x in range(0, 365)}
    for event in events:
        if event.type == 'PushEvent':
            histogram[event.created_at.date()] += 1

    streak_days = 0
    for date in date_list[1:]:
        if histogram[date] == 0:
            break
        streak_days += 1
    if histogram[base.date()] > 0:
        streak_days += 1

    for event in events:
        if event.type == 'PushEvent':
            break

    today = datetime.datetime.utcnow()

    return render_template('reminders/settings.html', form=form,
        today=today.date(),
        event=event,
        histogram=histogram,
        date_list=date_list,
        streak_days=streak_days)
