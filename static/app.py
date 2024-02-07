from flask import Flask, render_template, jsonify, request
from flask import Markup
from flask_cors import CORS
import requests, psycopg2
import sqlalchemy
from sqlalchemy import create_engine, text
import psycopg2
import pickle
import pandas as pd


#################################################
# Flask Setup
#################################################
app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
CORS(app)

#Connect to the database using psycopg2
def connect_to_database():
    try:
        conn = psycopg2.connect(host= 'localhost',
        user =  'postgres',
        password=  'postgres',
        dbname = "listings_db",
        port =  5432
    )
        return conn
    except Exception as error:
        print(f"Error: Unable to connect to the dataBase - {str(error)}")
        raise ConnectionError(f"Error: Unable to connect to the Database - {str(error)}")

#Render in HTML template
@app.route("/")
def home():
    return render_template('html/home.html') 

#fetch unique neighbourhoods from DB to fill drop-down
@app.route("/api/get_neighbourhoods", methods = ['GET'])
def get_neighbourhoods():
    connection = connect_to_database()

    if connection:
        try:
            query = "SELECT DISTINCT neighbourhood FROM toronto_listings;"
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

#generate predictions based on drop-down selections
@app.route("/predict_Price")
def predict_Price():

    #Get Arguments
    beds = request.args.get("beds", type=int)
    baths = request.args.get("baths", type=int)
    dens = request.args.get("dens", type=int)
    neighbourhood = request.args.get("neighbourhood", type=text)
    property_type = request.args.get("property_type", type=text)


    pkl_model = "housingModel.pkl"  
    with open(pkl_model, 'rb') as file:  
        housingModel = pickle.load(file)

    neighbourhood_key = "neighbourhood_" + neighbourhood
    property_type_key = "property_type_" + property_type

    house_dict = {"beds": beds,
                  "baths": baths,
                  "dens": dens,
                  neighbourhood_key: neighbourhood,
                  property_type_key: property_type}
    
    X = pd.DataFrame(house_dict)

    prediction = housingModel.predict(X)

    return prediction
    
if __name__ == "__main__":
    app.run(debug=False)