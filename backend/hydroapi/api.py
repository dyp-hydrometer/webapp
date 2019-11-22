"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request
from flask import current_app as app
import sys
from .models import db, Hydrometer, Data, Profile
from datetime import datetime

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
        hydrometer.mac_addr = data["mac_addr"]
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
        h_data = [x.to_dict() for x in hydrometer.data.filter(Hydrometer.brew_start >= hydrometer.brew_start).all()]
        return jsonify({'hydrometer': hydrometer.to_dict(), 'data': h_data })
    elif request.method == 'PUT':
        data = request.get_json()

        # if the user is updating a value such as activity or update interval
        if "battery" in data:
            hydrometer.battery = data["battery"]
        hydrometer.color = data["color"]

        hydrometer.interval = data["interval"]

        # data: none, hydro: 1

        if data["active"] is True:
            if hydrometer.active is False:
                if data["profile"] is None:
                    return jsonify(error="Cannot start a brew without first setting a profile"), 409
                if hydrometer.profile != data["profile"]:
                    hydrometer.profile = data["profile"]
                
                hydrometer.active = True
                hydrometer.brew_start = str(datetime.utcnow())
            elif hydrometer.active is True:
                if data["profile"] != hydrometer.profile:
                    return jsonify(error="Cannot change profile while a brew is active"), 409
        else:
            if hydrometer.active is True:
                hydrometer.active = False
                hydrometer.profile = data["profile"]
            else:
                hydrometer.profile = data["profile"]

        try:
            db.session.add(hydrometer)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(error="Error commiting transaction"), 404

        # grab the new, updated row
        #hydrometer = Hydrometer.query.get(id)
        return '', 200

@api.route('/hydrometers/<mac_addr>/')
def hydrometer_mac(mac_addr):
    """
        Return associated hydrometer data by mac address, used by the bluetooth connection manager
    """
    hydrometer = Hydrometer.query.filter(Hydrometer.mac_addr == mac_addr).first()
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404
    return jsonify(hydrometer.to_dict())

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

@api.route('/hydrometers/<int:id>/<string:key>', methods=('GET', 'PUT', 'POST'))
def hydrometer_key(id, key):
    """
        Return the specified hydrometer value by key
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    if request.method == 'GET':
        return_data = None
        try:
            # data is a special case since it is lazy loaded
            if key == "data":
                return_data = [x.to_dict() for x in hydrometer.data.filter(Hydrometer.brew_start >= hydrometer.brew_start).all()]
            else:
                return_data = {key: hydrometer.to_dict()[key]}
        except:
            return jsonify(error="No such c in hydrometer"), 404
        finally:
            return jsonify(return_data)

    elif request.method == 'PUT' or request.method == 'POST':
        data = None
        try:
            data = request.get_data().decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            data = request.get_json()

        if key == "color":
            hydrometer.color = data
        elif key == "active":
            # will be a string if decode() is used, else will be boolean if get_json() is used
            if data == "true" or data is True:
                if hydrometer.profile is None:
                    return jsonify(error="Cannot start a brew without first setting a profile"), 409
                hydrometer.brew_start = str(datetime.utcnow())
            elif data == 'false' or data is False:
                if hydrometer.profile is not None:
                    hydrometer.profile = None
                hydrometer.active = False
            else:
                return jsonify(error="Unexpected input for boolean key"), 400
        elif key == "battery":
            hydrometer.battery = data
        elif key == "interval":
            hydrometer.interval = data
        elif key == "profile":
            if hydrometer.active is True:
                return jsonify(error="There is already a brew in progress. Stop it to make changes to the brew profile"), 409
            hydrometer.profile = data

        try:
            db.session.add(hydrometer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error="Error commiting transaction"), 404

        # grab the new, updated row
        #hydrometer = Hydrometer.query.get(id)
        return '', 200

@api.route('/hydrometers/<int:id>/data/last')
def hydrometer_last(id):
    """
        Return the last data entry from the hydrometer
    """
    hydrometer = Hydrometer.query.get(id)
    if hydrometer is None:
        return jsonify(error="No such hydrometer"), 404

    # lazy load the hydrometer data
    h_data = hydrometer.data.filter(Hydrometer.brew_start >= hydrometer.brew_start).order_by(Data.id.desc()).limit(1)[0]
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

    try:
        db.session.add(reading)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(error="Error commiting transaction"), 404
    return jsonify(reading=reading), 201

@api.route('/profiles/', methods=('GET', 'POST'))
def fetch_profiles():
    """
        Return all saved profiles,
        Add a new profile by name
    """
    if request.method == 'GET':
        profiles = Profile.query.order_by(Profile.id).all()
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
        return jsonify(profile.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()

        profile.name = data['name']
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