"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request
from flask import current_app as app
import sys
from .models import db, Hydrometer, Data, Profile

api = Blueprint('api', __name__)

@api.route('/hydrometers/', methods=('GET', 'POST'))
def fetch_hydrometers():
    """
        Return all saved hydrometers,
        Add a new hydrometer by color
    """
    if request.method == 'GET':
        hydrometers = Hydrometer.query.order_by(Hydrometer.id).all()
        return jsonify([h.to_dict() for h in hydrometers])
    elif request.method == 'POST':
        data = request.get_json()

        hydrometer = Hydrometer(color=data['color'])
        hydrometer.battery = data['battery']
        hydrometer.interval = app.config['INTERVAL_DEFAULT']

        db.session.add(hydrometer)
        db.session.commit()

        return jsonify(hydrometer.to_dict()), 201

@api.route('/hydrometers/<int:id>/', methods=('GET', 'PUT'))
def hydrometer(id):
    """
        Return associated hydrometer data by id,
        Update hydrometer info
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    if request.method == 'GET':
        # lazy load the hydrometer data
        h_data = [x.to_dict() for x in hydrometer.data.all()]
        return jsonify({'hydrometer': hydrometer.to_dict(), 'data': h_data })
    elif request.method == 'PUT':
        data = request.get_json()

        # if the user is updating a value such as activity or update interval
        if "battery" in data:
            hydrometer.battery = data["battery"]
        hydrometer.color = data["color"]
        hydrometer.active = data["active"]
        hydrometer.profile = data["profile"]
        hydrometer.interval = data["interval"]

        try:
            db.session.add(hydrometer)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(error="Error commiting transaction"), 404

        # grab the new, updated row
        #hydrometer = Hydrometer.query.get(id)
        return '', 201

@api.route('/hydrometers/<int:id>/info')
def hydrometer_info(id):
    """
        Return associated hydrometer info by id,
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    # lazy load the hydrometer data
    return jsonify(hydrometer.to_dict())

@api.route('/hydrometers/<int:id>/<string:key>')
def hydrometer_key(id, key):
    """
        Return the specified hydrometer's battery status
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404
    
    data = None
    try:
        if key == "data":
            data = [x.to_dict() for x in hydrometer.data.all()]
        else:
            data = hydrometer.to_dict()[key]
    except:
        return jsonify(error="No such key in hydrometer"), 404
    finally:
        return jsonify(data)

@api.route('/hydrometers/<int:id>/data/last')
def hydrometer_last(id):
    """
        Return the last data entry from the hydrometer
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    # lazy load the hydrometer data
    h_data = hydrometer.data.order_by(Data.id.desc()).limit(1)[0]
    return jsonify(h_data.to_dict())

@api.route('/hydrometers/<int:id>/reading/', methods=('PUT',))
def reading(id):
    '''
        Insert a new data row for a sensor reading
    '''
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    data = request.get_json()

    reading = Data(hydrometer_id = id)

    reading.specific_gravity = data["specific_gravity"]
    reading.time = data["time"]
    reading.temp = data["temp"]
    reading.rssi = data["rssi"]

    try:
        db.session.add(reading)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(error="Error commiting transaction"), 404
    return '', 201

@api.route('/profiles/', methods=('GET', 'POST'))
def fetch_profiles():
    """
        Return all saved profiles,
        Add a new profile by name
    """
    if request.method == 'GET':
        profiles = Profile.query.all()
        return jsonify([p.to_dict() for p in profiles])
    elif request.method == 'POST':
        data = request.get_json()

        profile = Profile(name=data['name'])
        profile.description = data['description']
        profile.req_temp = data['req_temp']
        profile.req_gravity = data['req_gravity']
        profile.duration = data['duration']

        try:
            db.session.add(profile)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(error="Error commiting transaction"), 404
        return '', 201

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
        profile.req_temp = r['req_temp']
        profile.req_gravity = r['req_gravity']
        profile.duration = r['duration']

        try:
            db.session.add(profile)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(error="Error commiting transaction"), 404

        return '', 201
