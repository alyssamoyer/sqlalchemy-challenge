import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#references to tables
Station = Base.classes.station
Measurement = Base.classes.measurement

#Flask App
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)


#home page that lists all routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<string:start>/<string:end>"
      
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement table for all dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp ).all()

    session.close()

    # Create a dictionary from the queried data. 
    # Loop through results and add dictionary value with date as key and prcp as value.
    precip_dates = []
    for date, prcp in results:
        date_dict = {}
        date_dict[date] = prcp
        precip_dates.append(date_dict)

#return the jsonified dictionary
    return jsonify(precip_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query to find the most recent date and calculate 365 days before with datetime.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_dt = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    start_dt = recent_dt - dt.timedelta(365)

    # Query measurement table for all dates and tobs from the last year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between(start_dt, recent_dt)).all()

    session.close()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<string:start>")
def dates(start):

    start_s = str(start)

    # Create our session (link) from Python to the DB
    session = Session(engine)


    #using the user provided start date query for the min, avg, and max temperatures in the time range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_s).all()
    
    

    session.close()

    # Convert list of tuples into normal list
    stats_list = list(np.ravel(results))

    return jsonify(stats_list)

@app.route("/api/v1.0/<string:start>/<string:end>")
def dates_between(start, end):

    start_s = str(start)
    end_s = str(end)

    # Create our session (link) from Python to the DB
    session = Session(engine)


    #using the user provided start and end date query for the min, avg, and max temperatures in the time range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date.between(start_s, end_s)).all()
    
    

    session.close()

    # Convert list of tuples into normal list
    statsb_list = list(np.ravel(results))

    return jsonify(statsb_list)