#!/usr/bin/env python3
""" Basic Babel setup"""

from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """ Represents a Flask Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def hello_world() -> str:
    """ rendering hello world"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run()
