# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import os
import json

import requests
from flask import Blueprint, flash, redirect, session, render_template, request, url_for

from codestreak.reminder.models import Reminder

blueprint = Blueprint('public', __name__, static_folder='../static')

# Auth0 Integration
# -----------------
auth_id = os.environ['AUTH0_CLIENT_ID']
auth_secret = os.environ['AUTH0_CLIENT_SECRET']
auth_callback_url = os.environ['AUTH0_CALLBACK_URL']
auth_domain = os.environ['AUTH0_DOMAIN']


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    return render_template('public/home.html',
        callback_url=auth_callback_url,
        auth_id=auth_id,
        auth_domain=auth_domain)


@blueprint.route('/about/')
def about():
    """About page."""
    return render_template('public/about.html',
                           callback_url=auth_callback_url,
                           auth_id=auth_id,
                           auth_domain=auth_domain)


@blueprint.route('/callback')
def callback_handling():
    code = request.args.get('code')

    json_header = {'content-type': 'application/json'}

    token_url = 'https://{0}/oauth/token'.format(auth_domain)
    token_payload = {
        'client_id': auth_id,
        'client_secret': auth_secret,
        'redirect_uri': auth_callback_url,
        'code': code,
        'grant_type': 'authorization_code'
    }

    # Fetch User info from Auth0.
    token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()
    user_url = 'https://{0}/userinfo?access_token={1}'.format(auth_domain, token_info['access_token'])
    user_info = requests.get(user_url).json()

    # Add the 'user_info' to Flask session.
    session['profile'] = user_info

    nickname = user_info['nickname']
    userid = user_info['user_id']


    if not Reminder.query.filter_by(slug=nickname).first():
        Reminder.create(slug=nickname, auth_id=userid)
    # if not storage.Inbox.does_exist(nickname):
    #     # Using nickname by default, can be changed manually later if needed.
    #     storage.Inbox.store(nickname, userid)

    return redirect(url_for('reminder.settings'))
