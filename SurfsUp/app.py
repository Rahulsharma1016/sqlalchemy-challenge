# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement 
Station =  Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Define a function which calculates and returns the the date one year from the most recent date
def date_prev_year():
    # Create the session
    session = Session(engine)

    # Define the most recent date in the Measurement dataset
    # Then use the most recent date to calculate the date one year from the last date
    most_recent_date = session.query(func.max(Measurement.date)).first()[0]
    first_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Close the session                   
    session.close()

    # Return the date
    return(first_date)


#################################################
# Flask Routes
#################################################
# define ("/")
@app.route("/")
def home():
    """Homepage - List all available api routes."""
    print("Request to homepage made...")
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"Static Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "<br/>"
        f"Dynamic Routes:<br/>"
        f" Start Route : /api/v1.0/yyyy-mm-dd<br/>"
        f"Start/end : /api/v1.0/yyyy-mm-dd/yyyy-mm-ddroute <br/>"
    )

# define ("/api/v1.0/precipitation")
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    prcp_data = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= date_prev_year()).all()
    
    session.close()

    prcp_list = [{"date": date, "prcp": prcp} for date, prcp in prcp_data]

  # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)


 
# define ("/api/v1.0/stations")
 
@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(Station.station).all()

    # Close the session                   
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))

    # Return a list of jsonified station data
    return jsonify(station_list)


# define ("/api/v1.0/tobs")

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)

    # Query tobs data from the last 12 months from the most recent date in the Measurement table
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
                        .filter(Measurement.station == 'USC00519281')\
                        .filter(Measurement.date >= date_prev_year()).all()

    # Close the session                   
    session.close()

    # Use list comprehension to create the list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]

    # Return a list of jsonified tobs data for the previous 12 months
    return jsonify(tobs_list)

# Define start date or start-end range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None, end=None):

    session = Session(engine)
    
    # Make a list to query (the minimum, average and maximum temperature)
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Check if there is an end date then do the task accordingly
    if end == None: 
        # Query the data from start date to the most recent date
        start_data = session.query(*sel).\
                            filter(Measurement.date >= start).all()
        # Convert list of tuples into normal list
        start_list = list(np.ravel(start_data))

        # Return a list of jsonified minimum, average and maximum temperatures for a specific start date
        return jsonify(start_list)
    else:
        # Query the data from start date to the end date
        start_end_data = session.query(*sel).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()
        # Convert list of tuples into normal list
        start_end_list = list(np.ravel(start_end_data))

        # Return a list of jsonified minimum, average and maximum temperatures for a specific start-end date range
        return jsonify(start_end_list)

    # Close the session                   
    session.close()


# Define main branch 
if __name__ == '__main__':
    app.run()

