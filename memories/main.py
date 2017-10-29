#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""A memory collection app."""

import hashlib

from flask import Flask
from flask import redirect
from flask import render_template
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


@app.route('/login', methods=['GET'])
def login():
    """Ask for login information."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    """Check the login information."""
    if 'username' not in request.values or 'password' not in request.values:
        # XXX add missing fields error
        return render_template('login.html')

    digest = hashlib.md5('{}:{}'.format(
        request.values['username'],
        request.values['password'])).hexdigest()
    if digest != app.config['LOGIN_INFO']:
        # XXX add wrong login error
        return render_template('login.html')

    session['login'] = digest
    return redirect(url_for('index'))
