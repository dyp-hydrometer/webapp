"""
models.py
- Data classes for the hydroapi application
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()

class Hydrometer(db.Model):
    __tablename__ = 'hydrometers'

    id = db.Column(db.Integer, primary_key=True)
    mac_addr = db.Column(postgresql.MACADDR, unique=True)
    color = db.Column(db.String(7))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    battery = db.Column(db.Float)
    # each hydrometer can have its interval changed individually
    interval = db.Column(db.Interval)
    data = db.relationship('Data', backref="hydrometers", lazy='dynamic')
    profile = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def to_dict(self):
        return dict(id = self.id,
                    mac_addr = self.mac_addr,
                    color = self.color,
                    created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    active = self.active,
                    battery = self.battery,
                    interval = str(self.interval),
                    profile = self.profile,
        )

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    hydrometer_id = db.Column(db.Integer, db.ForeignKey("hydrometers.id"))
    temp = db.Column(db.Float)
    specific_gravity = db.Column(db.Float)
    # store here as well in case the user changes the value during use
    time = db.Column(db.DateTime, default=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    # signal strength
    rssi = db.Column(db.SmallInteger)

    def to_dict(self):
        return dict(id = self.id,
                    hydrometer_id = self.hydrometer_id,
                    temp = self.temp,
                    specific_gravity = self.specific_gravity,
                    time = str(self.time),
                    rssi = self.rssi
        )

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    req_temp = db.Column(db.Float)
    req_gravity = db.Column(db.Float)
    duration = db.Column(db.Interval)

    def to_dict(self):
        return dict(id = self.id,
                    name = self.name,
                    description = self.description,
                    req_temp = self.req_temp,
                    req_gravity = self.req_gravity,
                    duration = str(self.duration),
        )