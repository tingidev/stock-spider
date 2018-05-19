# flask/flask_app.py

from flask import Flask, render_template
from models import db, Listing

# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config.from_pyfile('settings.cfg')
app.debug = True

# initalize app with database
db.init_app(app)
db.connect(connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
print(app.instance_path)
print(app.root_path)
print(app.static_url_path)

@app.route("/")
def index_by_date():
    ## get the last date the webscraper was run
    for listing in Listing.objects().fields(date_str=1).order_by('-date_str').limit(1):
        day_to_pull = listing.date_str

    return render_template(
        'index-by-date.html',
        Listing = Listing,
        day_to_pull = day_to_pull
        )

@app.route("/") 
def index_by_loc():
    ## get the last date the webscraper was run
    for listing in Listing.objects().fields(loc=1).order_by('-loc').limit(1):
        loc_to_pull = listing.loc

    return render_template(
        'index-by-loc.html',
        Listing = Listing,
        loc_to_pull = loc_to_pull
        )

@app.route("/date")
def all_dates():
    ## get all the dates the scraper was run on
    dates = Listing.objects().fields(date_str=1).distinct('date_str')
    return render_template(
        'all-dates.html',
        dates = reversed(sorted(list(dates))) #latest date on top
        )

@app.route("/location")
def all_locs():
    ## get all the locations the scraper was run on
    locs = Listing.objects().fields(loc=1).distinct('loc')
    return render_template(
        'all-locs.html',
        locs = list(locs) #latest date on top
        )  

@app.route("/date/<day_to_pull>")
def by_date(day_to_pull=None):
    ## display only selected date
    return render_template(
        'index-by-date.html',
        Listing = Listing,
        day_to_pull = day_to_pull
        )

@app.route("/location/<loc_to_pull>")
def by_location(loc_to_pull=None):
    dates = Listing.objects().fields(date_str=1).distinct('date_str')
    return render_template(
        'index-by-loc.html',
        Listing = Listing,
        loc_to_pull = loc_to_pull,
        dates = reversed(sorted(list(dates))) #latest date on top
        )

@app.route("/source")
def index_source():
    ## get all the dates the scraper was run on
    return render_template(
        'index-source.html',
        )

@app.route("/plots")
def index_plots():
    ## get all the dates the scraper was run on
    return render_template(
        'index-plots.html',
        )

if __name__ == "__main__":
    app.run()