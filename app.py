from distutils.log import debug
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#flask
app = Flask(__name__)

#create engine
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect on existing database
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#home route
@app.route('/')
def home():
    return(
            f'<center><h2>Welcome to my Module 10 Challenge -API</center></h2>'
            f'<center><h3>Available Routes</center></h3>'
            f'<center>/api/v1.0/precipitation</center>'
            f'<center>/api/v1.0/stations</center>'
            f'<center>/api/v1.0/tobs</center>'
            f'<center>/api/v1.0/start/end</center>'
       )
#/api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date,Measurement.prcp).\
              filter(Measurement.date >= previousYear). all()
    #close session
    session.close()
    #dictionary
    precipitationList = {date: prcp for date, prcp in results}
    #return jsonify
    return jsonify(precipitationList)
#/api/v1.0/stations route
@app.route("/api/v1.0/stations")
def station():
    # Perform a query to retrieve the name of stations
    results = session.query(Station.station).all()
    session.close()

    stationList = list(np.ravel(results))
    #jsonify result
    return jsonify(stationList)

#/api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():
    previousYear = dt.date(2017,8,23)-dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previousYear).all()
    session.close()
    temperatureList = list(np.ravel(results))
    return jsonify(temperatureList)

#/api/v1.0/start/end route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    selection = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    if not end:
        startDate=dt.datetime.strptime(start,"%m%d%y")
        results = session.query(*selection). filter(Measurement.date >= startDate). all()
        session.close()
        temperatureList = list(np.ravel(results))
        return jsonify(temperatureList)
    else:
        startDate=dt.datetime.strptime(start,"%m%d%y")
        endDate=dt.datetime.strptime(end,"%m%d%y")
        results = session.query(*selection).\
         filter(Measurement.date >= startDate).\
         filter(Measurement.date<= endDate). all()
        session.close()
        temperatureList = list(np.ravel(results))
        return jsonify(temperatureList)


#launch
if __name__ == '__main__':
    app.run(debug = True)
