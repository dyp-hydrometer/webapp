"""
models.py
- Data classes for the hydroapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hydrometer(db.Model):
    __tablename__ = 'hydrometers'

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    battery = db.Column(db.Float)
    # each hydrometer can have its interval changed individually
    interval = db.Column(db.Interval)
    data = db.relationship('Data', backref="hydrometers", lazy=False)
    profile = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def to_dict(self):
        return dict(id = self.id,
                    colorname = self.color,
                    created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    active = self.active,
                    battery = self.battery,
                    interval = str(self.interval),
                    data = [point.to_dict() for point in self.data],
                    profile = self.profile
        )

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    hydrometer_id = db.Column(db.Integer, db.ForeignKey("hydrometers.id"))
    temp = db.Column(db.Float)
    angle = db.Column(db.Float)
    # store here as well in case the user changes the value during use
    interval = db.Column(db.Interval)
    # signal strength
    rssi = db.Column(db.SmallInteger)

    def to_dict(self):
        return dict(id = self.id,
                    hydrometer_id = self.hydrometer_id,
                    temp = self.temp,
                    angle = self.angle,
                    interval = str(self.interval),
                    rssi = self.rssi
        )

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    requirements =  db.relationship('Requirement', backref='profiles', lazy=False)

    def to_dict(self):
        return dict(id = self.id,
                    name = self.name,
                    description = self.description,
                    requirements = [requirement.to_dict() for requirement in self.requirements]
        )

class Requirement(db.Model):
    __tablename__ = 'requirements'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"))
    req_temp = db.Column(db.Float)
    req_gravity = db.Column(db.Float)
    duration = db.Column(db.Interval)

    def to_dict(self):
        return dict(id = self.id,
                    profile_id = self.profile_id,
                    req_temp = self.req_temp,
                    req_gravity = self.req_gravity,
                    duration = str(self.duration),
        )

'''
class Settings(db.Model):
    __tablename__ = 'settings'

    notify = db.Column(db.Boolean)
    # default dispaly unit. Enum?
    units = db.Column(db.Enum('SG', 'Plato', 'Brix'))
    # default update interval
    default_interval = db.Column(db.Interval)

    def to_dict(self):
        return dict(notify = self.notify,
                    units = self.units,
                    default_interval = self.default_interval
        )
'''