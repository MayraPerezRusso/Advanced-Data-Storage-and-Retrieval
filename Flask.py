import numpy as np
import datedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
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

@app.route("/")
def WELCOME():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all Precipitation by date"""
    results = session.query(Measurement.date,Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_prcp=[]
    for result in results:
        row["Date"]=results[0]
        row["prcp"]=results[1]
        all_prcp.append(row)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    results2 = session.query(Measurement.station).group_by(Measurement.station).all()

    all_station = list(np.ravel(results2))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    twelvemonths_agoday = dt.datetime.strptime(last_day, '%Y-%m-%d') - datedelta.MONTH*12

    results3 = session.query(Measurement.tobs).\
        filter(Measurement.date > twelvemonths_agoday).all()
   
    all_tobs = list(np.ravel(results3))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def date(start):
   
    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    all_info = list(np.ravel(results4))    
    return jsonify(all_info)

@app.route("/api/v1.0/<start>/<end>")
def date2(start,end):
   
    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_info2 = list(np.ravel(results5))    
    return jsonify(all_info2)

if __name__ == '__main__':
    app.run()
