# flask/app.py

from flask import Flask, render_template
from models import db, Listing

# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_SETTINGS'] = {
    'db': 'tingi-sandbox',
    'host': 'localhost',
    'port': 27017
}
app.debug = True

# initalize app with database
db.init_app(app)

@app.route("/")
def index():
    ## get the last date the webscraper was run
    for listing in Listing.objects().fields(date_str=1).order_by('-date_str').limit(1):
        day_to_pull = listing.date_str

    return render_template(
        'index.html',
        Listing = Listing,
        day_to_pull = day_to_pull
        )

@app.route("/date")
def all_dates():
    ## get all the dates the scraper was run on
    dates = Listing.objects().fields(date_str=1).distinct('date_str')

    return render_template(
        'all_dates.html',
        dates = reversed(list(dates)) #latest date on top
        )

@app.route("/date/<day_to_pull>")
def by_date(day_to_pull=None):
    ## display only selected date
    return render_template(
        'index.html',
        Listing = Listing,
        day_to_pull = day_to_pull
        )

@app.route("/loc")
def all_locs():
    ## get all locations the scraper was run on
    locs = Listing.objects().fields(loc=1).distinct('loc')

    return render_template(
        'all-locs.html',
        locs = sorted(list(locs), key=str.lower) #sort list of locations
        )

@app.route("/loc/<loc_to_pull>")
def by_location(loc_to_pull=None):
    return render_template(
        'by_location.html',
        Listing = Listing,
        loc = loc_to_pull
        )

if __name__ == "__main__":
    app.run()