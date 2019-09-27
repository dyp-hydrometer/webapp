"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request
from flask import current_app as app
from .models import db, Hydrometer, Data, Profile, Requirement

api = Blueprint('api', __name__)

@api.route('/hello/<string:name>/')
def say_hello(name):
    """
    Dummy test
    """
    response = { 'msg': "Hello, {}.".format(name.capitalize()) }
    return jsonify(response)

@api.route('/hydrometers/', methods=('GET', 'POST'))
def fetch_hydrometers():
    """
        Return all saved hydrometers,
        Add a new hydrometer by color
    """
    if request.method == 'GET':
        hydrometers = Hydrometer.query.all()
        return jsonify({ 'hydrometers': [h.to_dict() for h in hydrometers]})
    elif request.method == 'POST':
        data = request.get_json()

        hydrometer = Hydrometer(color=data['color'])
        hydrometer.battery = data['battery']
        hydrometer.interval = app.config['INTERVAL_DEFAULT']

        db.session.add(hydrometer)
        db.session.commit()

        print(hydrometer.to_dict())

        return jsonify(hydrometer.to_dict()), 201

@api.route('/hydrometers/<int:id>/', methods=('GET', 'PUT'))
def hydrometer(id):
    """
        Return associated hydrometer data by id,
        Update hydrometer info
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error=404), 404

    if request.method == 'GET':
        if hydrometer is None:
            return 
        return jsonify({ 'hydrometer': hydrometer.to_dict() })
    elif request.method == 'PUT':
        data = request.get_json()

        # if the user is updating a value such as activity or update interval
        hydrometer.battery = data["battery"]
        hydrometer.color = data["color"]
        hydrometer.active = data["active"]
        hydrometer.profile = data["profile"]

        db.session.commit()

        # grab the new, updated row
        hydrometer = Hydrometer.query.get(id)
        return jsonify(hydrometer.to_dict()), 201

@api.route('/hydrometers/<int:id>/reading/', methods=('PUT',))
def reading(id):
    '''
        Insert a new data row for a sensor reading
    '''
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error=404), 404

    reading = Data(hydrometer_id = id)
    reading.angle = data["angle"]
    reading.temp = data["temp"]
    reading.interval = data["interval"]
    reading.rssi = data["rssi"]

    hydrometer.battery = data["battery"]

    db.session.commit()

    # grab the new, updated row
    hydrometer = Hydrometer.query.get(id)
    return jsonify(hydrometer.to_dict()), 201

@api.route('/profiles/', methods=('GET', 'POST'))
def fetch_profiles():
    """
        Return all saved profiles,
        Add a new profile by name
    """
    if request.method == 'GET':
        profiles = Profile.query.all()
        return jsonify({ 'profiles': [p.to_dict() for p in profiles]})
    elif request.method == 'POST':
        data = request.get_json()

        profile = Profile(name=data['name'])
        profile.description = data['description']

        requirements = []
        for r in data['requirements']:
            requirement = Requirement(req_temp = r['req_temp'],
                                      req_sg = r['req_gravity'],
                                      duration = r['duration'])
            requirements.append(requirement)
        profile.requirements = requirements

        db.session.add(profile)
        db.session.commit()
        return jsonify(profile.to_dict()), 201

@api.route('/profiles/<int:id>/', methods=('GET', 'PUT'))
def profile(id):
    """
        Return all of a profile's information by id,
        Update a profile
    """
    profile = Profile.query.get(id)
    if profile is None:
        return jsonify(error=404), 404

    # return a profile's info by id
    if request.method == 'GET':
        return jsonify({ 'profile': profile.to_dict() })
    elif request.method == 'PUT':
        data = request.get_json()

        profile.name = data['name']
        profile.description = data['description']

        requirements = []
        for r in data['requirements']:
            requirement = Requirement(req_temp = r['req_temp'],
                                      req_sg = r['req_gravity'],
                                      duration = r['duration'])
            requirements.append(requirement)
        profile.requirements = requirements

        db.session.commit()

        # grab the new, updated row
        profile = Profile.query.get(data['id'])
        return jsonify(profile.to_dict()), 201
