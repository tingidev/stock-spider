# flask/models.py

from flask_mongoengine import MongoEngine

db = MongoEngine()

class Listing(db.Document):
    # Class for defining structure of stock listings

    date = db.DateTimeField(required=True)
    date_str = db.StringField(max_length=10, required=True)
    acronym = db.StringField(max_length=8, required=True)
    name = db.StringField(max_length=30, required=True)
    loc = db.StringField(max_length=3, required=True)
    pe_val = db.FloatField(required=True)
    volume = db.FloatField(required=True)
    price = db.FloatField(required=True)
    change = db.FloatField(required=True)

    meta = {
        'collection': 'stock_listings', # daily summary
        'ordering': ['-change'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }