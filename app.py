import numpy as np 
import dateline as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###############################################
# Database Setup
###############################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to the table
Measurement = Base.classes.measurement 

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routs:<br>"
        f"Measurements: /api/v1.0/temperature"
        f"Stations: /api/v1.0/stations"
        f"Temperatures in 2016-2017: /api/v1.0/temperature"
        f"Precipitation in 2016-2017: /api/v1.0/prcp"
    )

@ap.route("/api/v1.0/date")
def date():
    # Create our session link from python to the DB
    session = Session(engine)

    """ Return a list of all temperature measurements"""
    # Query all dates
    results = session.quiry(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    session.close()

    # Convert list of tuples into a normal list
    all_temperature = list(np.ravel(results))

    return jsonify(all_temperature)

@app.route("/api/v1.0/measurements")
def measurements():
# Create our session (link) from Python to the DB  
    session = Session(engine)

    """ Return a list of measurement data including the date, temperature and prcp of each measurement"""
    # Query all measurements
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).all()
    session.close()

# Create a dictionary from the row data and append to a list of all_measurements
all_measurements = []
for date, tobs, prcp in results:
    measurement_dict = {}
    measurement_dict["date"] = date
    measurement_dict["tobs"] = temperature
    measurement_dict["prcp"] = prcp
    all_measurement.append(measurement_dict)

return jsonify(all_measurements)

if __name__ == '__main__':
    app.run(debug = True)
    