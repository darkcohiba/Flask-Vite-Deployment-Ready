#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Yoga_Class, Yoga_SignUp, User, Community_Event, Community_Event_SignUp

def create_database():
 with app.app_context():
        db.create_all()

def create_yoga_classes():
    y1 = Yoga_Class(
        class_name = "Power Flow",
        class_description = "Empower yourself with this musically driven, soul nourishing, upbeat class. Flow with breath and dig deep for 60 fun and challenging minutes. All levels welcome. Class heated to 90 degrees +.",
        start_time = "",
        time_duration = "60 min.",
        teacher = ""
    )



if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
