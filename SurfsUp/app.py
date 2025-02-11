# Import the dependencies.
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session



#################################################
# Database Setup
#################################################
# Create the engine to connect to the database
engine= create_engine("sqlite:///Resources/hawaii.sqlite")


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
def welcome():
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
    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations (tobs)"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of the minimum, average, and maximum temperature for a given start date"""
    # Query the min, avg, and max temperatures for a given start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["min"] = min
        tobs_dict["avg"] = avg
        tobs_dict["max"] = max
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of the minimum, average, and maximum temperature for a given start and end date"""
    # Query the min, avg, and max temperatures for a given start and end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["min"] = min
        tobs_dict["avg"] = avg
        tobs_dict["max"] = max
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)
if __name__ == '__main__':
    app.run(debug=True)

