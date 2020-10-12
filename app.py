import numpy as np 
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)


# Flask Route setup

# define what to do when a user hits the index route
@app.route("/")
def home():
    # Add back end print statements
    print("Server received request for 'Home' page...")
    # print out all available routes
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create our session from python to the DB
    session = Session(engine)
    # Perform query then close connection
    results = session.query(Measurement.date, func.sum(Measurement.prcp)).filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).order_by(Measurement.date).all()
    session.close()

    # Create a dictionary from the query output
    prcp_results = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_results.append(prcp_dict)
    return jsonify(prcp_results)
        



if __name__ == '__main__':
    app.run(debug=True)