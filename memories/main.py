#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""A memory collection app."""

from flask import Flask

app = Flask(__name__)

app.config.from_object('memories.defaults')
app.config.from_envvar('MEMORIES_SETTINGS', silent=True)


@app.route('/')
def index():
    """The main page."""
    return 'Hello world'
