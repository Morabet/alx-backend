#!/usr/bin/env python3
""" Display the current time"""

import pytz
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g
from typing import Dict, Union


app = Flask(__name__)


class Config:
    """ Represents a Flask Babel configuration"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


def get_locale() -> str:
    """ Retrieves the locale for a web page"""
    # 1. Locale from URL parameters
    if 'locale' in request.args and request.args['locale'] in Config.LANGUAGES:
        return request.args['locale']
    # 2. Locale from user settings (assuming it's stored in the user object)
    if g.user and g.user['locale'] in Config.LANGUAGES:
        return g.user['locale']
    # 3. Locale from request header
    if request.headers.get('Accept-Language', None) and \
            request.headers.get('Accept-Language', None) in Config.LANGUAGES:
        return request.headers.get('Accept-Language')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_timezone() -> str:
    """ Retrieves the timezone for a web page"""
    if 'timezone' in request.args:
        try:
            tz = request.args['timezone']
            return pytz.timezone(tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and g.user.get('timezone', None):
        try:

            tz = g.user.get('timezone')
            return pytz.timezone(tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return Config.BABEL_DEFAULT_TIMEZONE


app.config.from_object(Config)
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)

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
    g.time = format_datetime()
    return render_template('index.html', user=g.user)


if __name__ == "__main__":
    app.run()
