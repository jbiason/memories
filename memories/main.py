#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""A memory collection app."""

from flask import Flask
from flask import redirect
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__)                           # pylint:disable=invalid-name

app.config.from_object('memories.defaults')
app.config.from_envvar('MEMORIES_SETTINGS', silent=True)


@app.before_request
def check_login():
    """Check if there is a login information in the session; if there isn't,
    redirects to the login page.
    """
    app.logger.debug('Endpoint: %s', request.endpoint)
    if (('login' not in session or
         session['login'] != app.config['LOGIN_INFO']) and
            request.endpoint != 'login'):
        return redirect(url_for('login'))


@app.route('/')
def index():
    """The main page."""
    return 'Hello world'


@app.route('/login')
def login():
    """Ask for login information."""
    return 'Login'
