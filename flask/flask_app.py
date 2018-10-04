# flask/flask_app.py

# bokeh imports
import random
import pandas as pd
#from bokeh.embed import components
#from bokeh.plotting import figure
#from bokeh.resources import INLINE
#from bokeh.util.string import encode_utf8

# flask imports
from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
from models import Listing
from socket import gethostname

# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## Load the Iris Data Set
#iris_df = pd.read_csv("data/iris.csv", names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
#feature_names = iris_df.columns[0:-1].values.tolist()

## Create the main plot
#def create_figure(current_feature_name):
#    fig = figure(plot_width=600, plot_height=400)
#    fig.line(
#        x=range(len(iris_df[current_feature_name])),
#        y=iris_df[current_feature_name]
#        )

    # Set the x axis label
#    fig.xaxis.axis_label = current_feature_name

    # Set the y axis label
#    fig.yaxis.axis_label = 'Count'
#    return fig

## include db name in URI; _HOST entry overwrites all others
app.config.from_pyfile('settings.cfg')
app.debug = True

## initalize app with database
db = None

def get_db():
    ## initialize / refresh DB post-fork for server performance
    global db
    if db is None:
        db = MongoEngine()
        db.init_app(app)
        db.connect(connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    else:
        db.connect(connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)
    return db

@app.route("/")
def index():
    db = get_db()
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
    ## get all dates the scraper was run on
    dates = Listing.objects().fields(date_str=1).distinct('date_str')
    return render_template(
        'all-dates.html',
        dates = reversed(sorted(list(dates))) # latest date on top
        )

@app.route("/location")
def all_locs():
    ## get all locations the scraper was run on
    locs = Listing.objects().fields(loc=1).distinct('loc')
    return render_template(
        'all-locs.html',
        locs = list(locs)
        )

@app.route("/company")
def all_comps():
    ## get all companies the scraper was run on
    comps = Listing.objects().fields(name=1).distinct('name')
    return render_template(
        'all-comps.html',
        comps = sorted(list(comps)) # alphabetically
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
    ## display only selected location
    dates = Listing.objects().fields(date_str=1).distinct('date_str')
    return render_template(
        'index-by-loc.html',
        Listing = Listing,
        loc_to_pull = loc_to_pull,
        dates = reversed(sorted(list(dates))) #latest date on top
        )

@app.route("/company/<comp_to_pull>")
def by_comp(comp_to_pull=None):
    ## display only selected company
    dates = Listing.objects().fields(date_str=1).distinct('date_str')
    return render_template(
        'index-by-comp.html',
        Listing = Listing,
        comp_to_pull = comp_to_pull,
        dates = reversed(sorted(list(dates))) #latest date on top
        )

@app.route("/source")
def index_source():
    return render_template(
        'index-source.html',
        )

@app.route("/plots")
def index_plots():
    return render_template(
        'index-plots.html',
        )


#@app.route('/bokeh')
#def index_bokeh():
    # Determine the selected feature
#    current_feature_name = request.args.get("feature_name")
#    if current_feature_name == None:
#        current_feature_name = "Sepal Length"

    # Create the plot
#    plot = create_figure(current_feature_name)

    # Embed plot into HTML via Flask Render
#    script, div = components(plot)
#    return render_template("index-bokeh.html", script=script, div=div, feature_names=feature_names,
#        current_feature_name=current_feature_name)


#@app.route('/bokeh')
#def bokeh():

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
#    fig = figure(plot_width=600, plot_height=600)
#    fig.vbar(
#        x=[1, 2, 3, 4],
#        width=0.5,
#        bottom=0,
#        top=[1.7, 2.2, 4.6, 3.9],
#        color='navy'
#    )

    # grab the static resources
#    js_resources = INLINE.render_js()
#    css_resources = INLINE.render_css()

    # render template
#    script, div = components(fig)
#    html = render_template(
#        'fresh-plots.html',
#        plot_script=script,
#        plot_div=div,
#        js_resources=js_resources,
#        css_resources=css_resources,
#    )
#    return encode_utf8(html)


################################

if __name__ == "__main__":
    app.run()
