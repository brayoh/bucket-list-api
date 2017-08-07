from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from app import db


class User(db.Model):
    """This class represents the users database table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow().isoformat())
    bucketlist = db.relationship('BucketList', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class BucketList(db.Model):
    """This is class represents the bucketlist database table."""

    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship('Item', backref='bucketlist',
                            cascade='all, delete', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow().isoformat())

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id


class Item(db.Model):
    """This class represents bucketlist items table. """

    __tablename__ = 'bucketlist_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlist.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow().isoformat())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
