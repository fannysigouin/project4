# Group 1 - Toronto Real Estate Listings Project 

## Overview

This project involves the collection, cleaning, and analysis of Toronto real estate listings data. The goal is to extract valuable insights from the data and create a machine learning model to predict property prices.

## Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [Data Collection](#data-collection)
- [Data Cleaning](#data-cleaning)
- [Database Creation](#database-creation)
- [Modeling](#modeling)
- [Deployment](#deployment)
- [Contributors](#contributors)
- [Data Collection](#data-collection-1)
- [Data Cleaning](#data-cleaning-1)
- [Database Creation](#database-creation-1)
- [Modeling](#modeling-1)
- [Deployment](#deployment-1)
- [Web Development](#web-development)
- [General](#general)
- [Python Libraries](#python-libraries)

## Data Collection

The project collects Toronto real estate listings data from multiple sources, including web scraping and API requests. The collected data includes property details such as address, price, baths, beds, and geographical coordinates.

## Data Cleaning

The data cleaning process involves handling missing values, formatting issues, and extracting latitude and longitude using the Geoapify API. Additionally, luxury listings with more than 5 bathrooms or more than 4 beds were removed, and outliers were addressed using the Interquartile Range (IQR) method. The cleaned data is stored in CSV files in the `data` folder.

## Database Creation

The cleaned data is imported into a PostgreSQL database named `listings_db` using SQLAlchemy. The database has a table named `toronto_listings` with columns like `mls_id`, `property_type`, `address`, and more.

## Modeling

A Random Forest Regressor model has been implemented to predict property prices based on features such as baths, beds, dens, relative latitude, and relative longitude. The model's performance is evaluated using cross-validation, providing Mean Absolute Error (MAE) scores for each fold. Neighbourhood-wise analysis revealed varying ratios of prediction errors, with specific attention given to neighbourhoods with a small number of listings.

## Deployment

The machine learning model is deployed using a cloud-based infrastructure, specifically on Amazon Web Services (AWS). The deployment process involves the following steps:

1. **Model Serialization:** The trained Random Forest Regressor model is serialized using the `joblib` library. 
   
2. **Flask API Endpoint:** A Flask web application is set up to serve as an API endpoint for the machine learning model. The Flask application uses Flask and Flask-CORS to handle HTTP requests and responses, providing a seamless interaction with the deployed model.

3. **PostgreSQL Database Interaction:** SQLAlchemy is utilized to interact with the PostgreSQL database named `listings_db`. The database stores relevant information about Toronto real estate listings.

4. **API Usage:** Users can make HTTP POST requests to the Flask API endpoint, providing property features as input in the request body. The API will respond with predicted property prices.

5. **Containerization:** The serialized model, database creation script, and flask application are encapsulated within a Docker container, with dependencies specified in the `requirements.txt` file to ensure consistent and reproducible deployment across different environments. When running the container, the database is created and the flask app is started using gunicorn. The Docker image is then pushed to docker hub.

6. **Azure Web App:** The application is deployed using Azure Web App Services and the Docker image that is available via Docker Hub.

7. **URL:** [Toronto Real Estate Price Predictor](https://toronto-real-estate-predictor.azurewebsites.net/) 

## Contributors

- Fanny Sigouin 
- Jorge Nardy 
- Kamal Farran 
- Tania Barrera 

# References

## Data Collection

- [Geoapify API](https://www.geoapify.com/) - Used for geocoding addresses and obtaining latitude and longitude.
- [Listing.ca](https://www.listing.ca/) - Source of real estate data for Toronto listings.

## Data Cleaning

- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/) - Reference for data manipulation using Pandas.
- [Regular Expressions in Python](https://docs.python.org/3/library/re.html) - Guide for using regular expressions in Python.
- [Pathlib Documentation](https://docs.python.org/3/library/pathlib.html) - Documentation for working with file paths using Pathlib.

## Database Creation

- [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Official documentation for PostgreSQL.

## Modeling

- [Scikit-learn Documentation](https://scikit-learn.org/stable/) - Documentation for the Scikit-learn machine learning library.

## Deployment

- [Azure Documentation](https://learn.microsoft.com/en-us/azure/app-service/) - Azure App Service documentation for setting up and deploying the application.
- [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/) - Flask documentation for setting up API endpoint. 
- [Docker Documentation](https://docs.docker.com/) - Docker documentation for containerization in deployment. 

## Web Development 

- [Bootstrap Documentation](https://getbootstrap.com/docs/3.3/) - Bootstrap documentation for setting up HTML, CSS and Java framekwork. 

## General

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) - Reference for using SQLAlchemy for database interactions.
- [Side Navigation](https://www.w3schools.com/howto/howto_js_sidenav.asp) - Code used to create the side navigation.

## Python Libraries

- [Pandas](https://pandas.pydata.org/) - Powerful data manipulation library for Python.
- [NumPy](https://numpy.org/) - Library for numerical operations in Python.
- [Scikit-learn](https://scikit-learn.org/stable/) - Machine learning library for Python.
