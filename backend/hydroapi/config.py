"""
config.py
- settings for the flask application object
"""

class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://evan:dyp@localhost/dyp_web'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = 'dyphydrometer'

    # used when adding a new hydrometer
    INTERVAL_DEFAULT = '5 seconds'