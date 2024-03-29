"""
.. module:: application
    :platform: Linux
    :synopsis: creates a Flask app instance and registers the database object

.. moduleauthor:: Evan Campbell
"""

from flask import Flask
from flask_cors import CORS

def create_app(app_name='HYDRO_API'):
    app = Flask(app_name)
    app.config.from_object('hydroapi.config.BaseConfig')

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    from hydroapi.api import api
    app.register_blueprint(api, url_prefix="/api")

    from hydroapi.models import db
    db.init_app(app)

    return app