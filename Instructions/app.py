# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime
import datetime as dt 

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
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
#******HOME*******
@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Hawai Honolulu<br/>"
        f"******************************************<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"------------------------------------<br/>"
        f"/api/v1.0/stations<br/>"
        f"------------------------------------<br/>"
        f"/api/v1.0/tobs<br/>"
        f"------------------------------------<br/>"
        f"Enter Start Date (Year-Month-Day)<br/>"
        f"/api/v1.0/<start><br/>"
        f"------------------------------------<br/>"
        f"Enter Start and End Date (Year-Month-Day)<br/>"
        f"/api/v1.0/<start>/<end>"
        
    )
#*****Percipitation Route**********
#* Query for the dates and temperature observations from the last year.
    #* Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
        #* Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()

    prcp = []
    #Query percipitation
    for p in precipitation:
        prcp.append({'date':p[0], 'tobs':p[1]})

    return jsonify(prcp)

#*****Stations********
#* Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.name, Station.station)
    #Query stations
    slist = []
    for s in station:
        slist.append({'name':s[0], 'station':s[1]})

    return jsonify(slist)

#*******Tobs*******
#* Return a JSON list of Temperature Observations (tobs) for the previous year.

#*******Start OR Start-End Range**********
#* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #* When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start):

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.date(2017, 8, 23)
   
    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    #print(f"Minimum temp: {minimum}")
    TAVG = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # print(f"Average temp: {average}")
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    # print(f"Maximum temp: {maximum}")
    
    result = [{"Minimum":TMIN},{"Maximum":TMAX},{"Average":TAVG}]
    
    return jsonify(result)

    #* When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
   
    TMIN = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    #print(f"Minimum temp: {minimum}")
    TAVG = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start,end)).all()
    # print(f"Average temp: {average}")
    TMAX = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start,end)).all()
    # print(f"Maximum temp: {maximum}")
    
    result = [{"Minimum":TMIN},{"Maximum":TMAX},{"Average":TAVG}]
    
    return jsonify(result)    



if __name__ == '__main__':
    app.run(debug=True)