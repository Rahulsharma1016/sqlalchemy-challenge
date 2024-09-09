SurfsUp project uses SQLAlchemy to interact with a climate database, along with Pandas for data handling and Matplotlib for visualizations. The project is organized into two key components:

climate.ipynb, which is focused on analyzing and exploring climate data,
app.py, which sets up API routes for serving data.


Key Details:
climate.ipynb:


This file utilizes SQLAlchemy ORM for querying the database, along with Pandas and Matplotlib for performing climate data analysis and visualization.
app.py:



This Python script defines the following API routes:
Static Routes:
/api/v1.0/precipitation: Provides precipitation data.
/api/v1.0/stations: Returns a list of weather stations.
/api/v1.0/tobs: Offers temperature observations (TOBS) for a given period.
Dynamic Routes:
/api/v1.0/yyyy-mm-dd: Retrieves data starting from a specified date.
/api/v1.0/yyyy-mm-dd/yyyy-mm-dd: Returns data between a start and end date.
