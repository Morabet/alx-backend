#!/usr/bin/env python3
""" Mock logging in"""

from flask_babel import Babel
from flask import Flask, render_template, request, g
from typing import Union, Dict


app = Flask(__name__)


class Config:
    """ Represents a Flask Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """ Retrieves the locale for a web page"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """ Get user by id"""
    if 'login_as' in request.args:
        try:
            id = int(request.args['login_as'])
            return users.get(id, None)
        except ValueError:
            pass
    return None


@app.before_request
def before_request() -> None:
    """ Store the user """
    g.user = get_user()


@app.route('/')
def hello_world() -> str:
    """ rendering hello world"""
    return render_template('5-index.html', user=g.user)


if __name__ == "__main__":
    app.run()
