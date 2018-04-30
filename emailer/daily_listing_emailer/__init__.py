import os
import configparser
from mongoengine.connection import connect
from .data_model import Listing
from .render_template import render
from .mailgun_emailer import send_email

def email_last_scraped_listing():
    # mongodb params (using configparser)
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.cfg'))
    mlab_uri = config.get('MongoDB', 'mlab_uri')
    #MONGO_URI = 'mongodb://localhost:27017'
    
    # connect to db
    MONGO_URI = mlab_uri
    connect('tingi-sandbox', host=MONGO_URI)

    ## get last date of scraper run
    for listing in Listing.objects().fields(date_str=1).order_by('-date_str').limit(1):
        day_to_pull = listing.date_str

    ## get last and previous date of scraper run
    #listing = Listing.objects().fields(date_str=1).order_by('-date_str')    
    #day_to_pull = listing[0].date_str
    #day_to_pull_pre = listing[505].date_str

    ## pass vars, render template, and send
    context = {
        'day_to_pull': day_to_pull,
        #'day_to_pull_pre': day_to_pull_pre,
        'Listing': Listing,
    }
    html = render("template.html", context)
    send_email(html)