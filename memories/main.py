#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""A memory collection app."""

import hashlib
import os

from flask import Flask
from flask import flash
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
    app.logger.debug('Endpoint: %s, path: %s',
                     request.endpoint, request.full_path)
    if 'login' not in session:
        if not request.full_path.startswith(url_for('login')):
            return redirect(url_for('login'))


@app.route('/')
def index():
    """The main page."""
    content = os.listdir(app.config['STORAGE'])
    return render_template('index.html', dates=content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Ask for login information."""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if ('username' not in request.values or
                'password' not in request.values or
                not request.values['username'] or
                not request.values['password']):
            app.logger.debug('Missing values')
            flash('Missing values', 'alert')
            return render_template('login.html')

        digest = hashlib.md5(u'{}:{}'.format(
            request.values['username'],
            request.values['password']).encode('utf-8')).hexdigest()
        if digest != app.config['LOGIN_INFO']:
            app.logger.debug('login info no match')
            flash('Invalid login credentials', 'alert')
            return render_template('login.html')

        session['login'] = digest
        return redirect(url_for('index'))
