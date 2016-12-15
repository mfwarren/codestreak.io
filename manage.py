#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os
from glob import glob
from subprocess import call
import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Option, Server, Shell
from flask_script.commands import Clean, ShowUrls

from codestreak.app import create_app
from codestreak.database import db
from codestreak.settings import DevConfig, ProdConfig
from codestreak.reminder.models import Reminder

CONFIG = ProdConfig if os.environ.get('TEST_ENV') == 'prod' else DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and the User model by default."""
    return {'app': app, 'db': db, 'Reminder': Reminder}


@manager.command
def hourly_notification():
    from github import Github
    from codestreak.email import notify
    hub = Github()

    for reminder in Reminder.query.filter_by(enabled=True, email_enabled=True).all():
        hub_user = hub.get_user(reminder.slug)

        event = hub_user.get_public_events()[0]  # the most recent public event

        last_event_time = event.created_at
        last_event_time = last_event_time + datetime.timedelta(hours=-5)  # UTC offset for EST
        today = datetime.datetime.now() + datetime.timedelta(hours=-5)

        if last_event_time.day != today.day:
            notify('last commit was {}'.format(last_event_time), reminder.email)


class Lint(Command):
    """Lint and check code style with flake8 and isort."""

    def get_options(self):
        """Command line options."""
        return (
            Option('-f', '--fix-imports', action='store_true', dest='fix_imports', default=False,
                   help='Fix imports using isort, before linting'),
        )

    def run(self, fix_imports):
        """Run command."""
        skip = ['requirements']
        root_files = glob('*.py')
        root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
        files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

        def execute_tool(description, *args):
            """Execute a checking tool with its arguments."""
            command_line = list(args) + files_and_directories
            print('{}: {}'.format(description, ' '.join(command_line)))
            rv = call(command_line)
            if rv is not 0:
                exit(rv)

        if fix_imports:
            execute_tool('Fixing import order', 'isort', '-rc')
        execute_tool('Checking code style', 'flake8')


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('lint', Lint())

if __name__ == '__main__':
    manager.run()
