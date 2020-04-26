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
station = Base.classes.station
measurment = Base.classes.measurment

#Flask App
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)