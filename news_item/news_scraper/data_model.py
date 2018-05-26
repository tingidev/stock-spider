# news_item/news_scraper/data_model.py

from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField, URLField, ListField, IntField

class NewsListing(Document):
    #Class for defining structure of daily listings

    """
    date = DateTimeField(required=True)
    date_str = StringField(max_length=10, required=True)    
    brand = StringField(max_length=25, required=True)
    title = StringField(max_length=250, required=True)
    summary = StringField(max_length=5000, required=True)
    keywords = ListField(StringField(max_length=25),required=True)
    url = URLField(required=True)
    """
    #number = IntField()
    text = StringField(required=True)

    meta = {
        'collection': 'news_items', # daily summary
        'ordering': ['-date_str'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }