import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
    )

@app.route("/api/v1.0/precipitation")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
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

