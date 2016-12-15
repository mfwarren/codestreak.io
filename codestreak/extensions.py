# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from raven.contrib.flask import Sentry
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

csrf_protect = CsrfProtect()
db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
sentry = Sentry()
