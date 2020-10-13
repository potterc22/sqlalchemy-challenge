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
        f"This will display the last 12 months of precipitation data<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"This will display the list of weather stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"This will display the last years worth of temperature observations from station USC00519281<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"Given a start date, this will display the min, avg and max temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Given a start and end date, this will display the min, avg, and max temperature for dates between the start and end date inclusively<br/>"
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
        
@app.route("/api/v1.0/stations")
def stations():
    # create our session from python to the DB
    session = Session(engine)
    # Perform query then close connection
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # create our session from python to the DB
    session = Session(engine)
    # Perform query then close connection
    results = (session.query(Measurement.date, Measurement.tobs).
        filter(Measurement.station == 'USC00519281').
        filter(Measurement.date >= '2016-08-23').
        group_by(Measurement.date).order_by(Measurement.date)).all()
    session.close()

    # Create a dictionary from the query output
    tobs_results = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_results.append(tobs_dict)
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # create our session from python to the DB
    session = Session(engine)
    # Perform query then close connection
    results = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)).all()
    session.close()

    # Create a dictionary from the query output
    stats = []
    for minimum, average, maximum in results:
        stat_dict = {}
        stat_dict['Min'] = minimum
        stat_dict['Avg'] = average
        stat_dict['Max'] = maximum
        stats.append(stat_dict)
    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create our session from python to the DB
    session = Session(engine)
    # Perform query then close connection
    results = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end)).all()
    session.close()

    # Create a dictionary from the query output
    stats = []
    for minimum, average, maximum in results:
        stat_dict = {}
        stat_dict['Min'] = minimum
        stat_dict['Avg'] = average
        stat_dict['Max'] = maximum
        stats.append(stat_dict)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)