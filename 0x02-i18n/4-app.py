#!/usr/bin/env python3
""" Force locale with URL parameter"""

from flask_babel import Babel
from flask import Flask, render_template, request


app = Flask(__name__)


class Config:
    """ Represents a Flask Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


def get_locale() -> str:
    """ Retrieves the locale for a web page"""
    if 'locale' in request.args and request.args['locale'] in Config.LANGUAGES:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app.config.from_object(Config)
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def hello_world() -> str:
    """ rendering hello world"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run()
