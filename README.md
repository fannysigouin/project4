# Toronto Real Estate Listings Project

## Overview

This project involves the collection, cleaning, and analysis of Toronto real estate listings data. The goal is to extract valuable insights from the data and create a machine learning model to categorize property prices.

## Table of Contents

- [Data Collection](#data-collection) 
- [Data Cleaning](#data-cleaning) 
- [Database Creation](#database-creation) 
- [Modeling](#modeling) 
- [Deployment](#deployment) 
- [Contributors](#contributors) 
- [References](#references) 

## Data Collection

The project collects Toronto real estate listings data from multiple sources, including web scraping and API requests. The collected data includes property details such as address, price, baths, beds, and geographical coordinates.

## Data Cleaning

The data cleaning process involves handling missing values, formatting issues, and extracting latitude and longitude using the Geoapify API. Additionally, luxury listings with more than 5 bathrooms or more than 4 beds were removed, and outliers were addressed using the Interquartile Range (IQR) method. The cleaned data is stored in CSV files in the `data` folder.

## Database Creation

The cleaned data is imported into a PostgreSQL database named `listings_db` using SQLAlchemy. The database has a table named `toronto_listings` with columns like `mls_id`, `property_type`, `address`, and more.

## Modeling

A Random Forest Regressor model has been implemented to predict property prices based on features such as baths, beds, dens, relative latitude, and relative longitude. The model's performance is evaluated using cross-validation, providing Mean Absolute Error (MAE) scores for each fold. Neighbourhood-wise analysis revealed varying ratios of prediction errors, with specific attention given to neighbourhoods with a small number of listings.

## Deployment

Update once complete

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

- [AWS Documentation](https://docs.aws.amazon.com/) - AWS documentation for setting up instances and deploying applications.

## General

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) - Reference for using SQLAlchemy for database interactions.

## Python Libraries

- [Pandas](https://pandas.pydata.org/) - Powerful data manipulation library for Python.
- [NumPy](https://numpy.org/) - Library for numerical operations in Python.
- [Scikit-learn](https://scikit-learn.org/stable/) - Machine learning library for Python.
