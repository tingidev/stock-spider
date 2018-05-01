from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField, FloatField
# IntField, URLField

class Listing(Document):
    #Class for defining structure of daily listings

    date = DateTimeField(required=True)
    date_str = StringField(max_length=10, required=True)
    acronym = StringField(max_length=8, required=True)
    name = StringField(max_length=30, required=True)
    loc = StringField(max_length=3, required=True)
    pe_val = FloatField(required=True)
    volume = FloatField(required=True)
    price = FloatField(required=True)
    change = FloatField(required=True)

    meta = {
        'collection': 'listings', # daily summary
        'ordering': ['-change'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }