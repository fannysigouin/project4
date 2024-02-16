from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import psycopg2
from joblib import load
import pandas as pd
import lzma
import os

#################################################
# Flask Setup
#################################################
app = Flask(
    __name__,
    static_url_path = '/static',
    static_folder = 'static',
    template_folder='templates'
)
CORS(app)

#################################################
# Database Setup
#################################################
# Create engine to the database path
owner_username = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host_name_address = 'localhost'
db_name = 'listings_db'
engine = create_engine(f"postgresql://{owner_username}:{password}@{host_name_address}:5432/{db_name}")
# Check if the db exists
if database_exists(engine.url):
    print('Database connection was successful.')
else:
    print('Something went wrong.')

# Connect to the database using psycopg2
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host= host_name_address,
            user =  owner_username,
            password=  password,
            dbname = db_name,
            port =  5432
        )
        return conn
    except Exception as error:
        print(f"Error: Unable to connect to the Database - {str(error)}")
        raise ConnectionError(f"Error: Unable to connect to the Database - {str(error)}")

#################################################
# Routes
#################################################
# Render HTML template for home page
@app.route("/")
def home():
    return render_template('home.html') 

# Render HTML template for about us page
@app.route("/about")
def about():
    return render_template('about.html') 

# Fetch unique neighbourhoods from DB to fill drop-down
@app.route("/api/get_neighbourhoods", methods = ['GET'])
def get_neighbourhoods():
    connection = connect_to_database()

    if connection:
        try:
            query = '''
            SELECT DISTINCT neighbourhood
            FROM toronto_listings
            ORDER BY neighbourhood ASC;
            '''
            cursor = connection.cursor()
            cursor.execute(query)
            #fetch all of the rows
            data = cursor.fetchall()
            #return jsonified data
            return jsonify(data)
        except Exception as error:
            print(f"Error: Unable to fetch from database - {str(error)}")
        finally:
            connection.close()
    
    return jsonify({'error': 'Unable to connect to DB'})

@app.route("/api/get_coordinates", methods = ['GET'])
def get_coordinates(neighbourhood):
    connection = connect_to_database()

    if connection:
        try:
            neighbourhood_q = neighbourhood.replace("'", "''")
            query = "SELECT avg(latitude) as latitude, avg(longitude) as longitude FROM toronto_listings where neighbourhood = '" + neighbourhood_q + "';"
            cursor = connection.cursor()
            cursor.execute(query)
            #fetch all of the rows
            data = cursor.fetchall()
            #return jsonified data  
            return data
        except Exception as error:
            print(f"Error: Unable to fetch from database - {str(error)}")
        finally:
            connection.close()
    
    return jsonify({'error': 'Unable to connect to DB'})

# Generate predictions based on drop-down selections
@app.route("/predict_Price")
def predict_Price():

    # Get Arguments
    beds = request.args.get("beds", type=int)
    baths = request.args.get("baths", type=int)
    dens = request.args.get("dens", type=int)
    neighbourhood = request.args.get("neighbourhood", type=str)
    property_type = request.args.get("property_type", type=str)

    coordinates = get_coordinates(neighbourhood)

    (latitude, longitude) = coordinates[0]

    rel_latitude = latitude - 43
    rel_longitude = longitude + 79

    model_path = "resources/housingModel_jl.xz"  
    with lzma.open(model_path, 'rb') as file:
        housingModel = load(file)
    columns_path = "resources/fit_columns.joblib"
    with open(columns_path, 'rb') as file:
        fit_columns = load(file)

    house_dict = {}
    for index, element in enumerate(fit_columns):
            house_dict[element] = 0
    
    neighbourhood_key = "neighbourhood_" + neighbourhood
    property_type_key = "property_type_" + property_type

    house_dict[neighbourhood_key] = 1
    house_dict[property_type_key] = 1
    house_dict["beds"] = beds
    house_dict["baths"] = baths
    house_dict["dens"] = dens
    house_dict["rel_latitude"] = rel_latitude
    house_dict["rel_longitude"] = rel_longitude
    
    X = pd.DataFrame(house_dict, index=[0])

    try:
        prediction = housingModel.predict(X)
        prediction_string = f'${"{:,.2f}".format(prediction[0])}'
    except:
        prediction_string = ["Sorry, Not Enough Data is Available for " + neighbourhood + ".\nPlease choose a different neighbourhood."]

    return jsonify(prediction_string)
    
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80
        # , ssl_context='adhoc'
        # , debug=True
    )
