# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("In & Out of Home section.")
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-01-01/<br/>"
        f"/api/v1.0/2016-01-01/2016-12-31/"
    )

@app.route('/api/v1.0/precipitation/')
def precipitation():
    """Return precipitation data for the last year."""

    precipitation_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(precipitation_data, '%Y-%m-%d') - dt.timedelta(days=365)

    rain_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date).all()

    p_dict = dict(rain_data)
    print(f"Results for Precipitation - {p_dict}")
    print("Out of Precipitation section.")
    return jsonify(p_dict) 

@app.route('/api/v1.0/stations/')
def stations():
    """Return a list of stations."""
    
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    print("Out of Station section.")
    return jsonify(station_list)

@app.route('/api/v1.0/tobs/')
def tobs():
    """Return temperature observations for the last year for the most active station."""
    
    precipitation_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(precipitation_data, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= last_year)\
        .order_by(Measurement.date).all()
    print()
    print("Temperature Results for All Stations")
    print(temp_obs)
    print("Out of TOBS section.")
    return jsonify(temp_obs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route('/api/v1.0/<start_date>/')
def calc_temps_start(start_date):
    """Return min, avg, and max temperatures for all dates after the start date."""
    print(start_date)
    
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result_temp = session.query(*select).\
        filter(Measurement.date >= start_date).all()
    print()
    print(f"Calculated temp for start date {start_date}")
    print(result_temp)
    print("Out of start date section.")
    return jsonify(result_temp)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route('/api/v1.0/<start_date>/<end_date>/')
def calc_temps_start_end(start_date, end_date):
    """Return min, avg, and max temperatures for dates between the start and end date inclusive."""
    
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result_temp = session.query(*select).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    print()
    print(f"Calculated temp for start date {start_date} & end date {end_date}")
    print(result_temp)
    print("Out of start & end date section.")
    return jsonify(result_temp)

if __name__ == "__main__":
    app.run(debug=True)