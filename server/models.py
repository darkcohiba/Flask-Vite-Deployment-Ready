from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relationship
from config import db, bcrypt

# Models go here!


class Yoga_Class(db.Model, SerializerMixin):
    __tablename__ = 'yoga_class'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String)
    class_type = db.Column(db.String)
    class_description = db.Column(db.String)
    start_time = db.Column(db.DateTime, server_default=db.func.now())
    time_duration = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships

    #serialize rules

    #validations
    pass

class Yoga_SignUps(db.Model, SerializerMixin):
    __tablename__ = 'yoga_signups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    yoga_class_id = db.Column(db.Integer, db.ForeignKey('yoga_class.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    #relationships

    #serialize rules

    #validations
    pass

class Users(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    address = db.Column(db.String)
    pronouns = db.Column(db.String)
    role = db.Column(db.String)
    membership_status = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships
    yoga_signups = relationship('Yoga_SignUps', backpopulates=('users'))
    event_signups = relationship()

    #serialize rules
    serialize_rules = ('-yoga_signups', '-event_signups',)

    #validations

class Event_Signups(db.Model, SerializerMixin):
    __tablename__ = 'event_signups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('community_events.id'))
    user_status = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    #relationships

    #serialize rules

    #validations
    pass

class Community_Events(db.Model, SerializerMixin):
    __tablename__ = 'community_events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    event_description = db.Column(db.String)
    start_time = db.Column(db.DateTime, server_default=db.func.now())
    time_duration = db.Column(db.String)
    location = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationships

    #serialize rules

    #validations
    pass