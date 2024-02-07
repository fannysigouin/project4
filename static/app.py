from flask import Flask, render_template, jsonify, request
from flask import Markup
from flask_cors import CORS
import requests, psycopg2
import sqlalchemy
from sqlalchemy import create_engine, text
import psycopg2
import pickle
import pandas as pd
import lzma


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
    neighbourhood = request.args.get("neighbourhood", type=str)
    property_type = request.args.get("property_type", type=str)

    pkl_model = "../model/housingModel_pkl.xz"  
    with lzma.open(pkl_model, 'rb') as file:
        housingModel = pickle.load(file)

    columns_path = "../model/fit_columns.pkl"
    with open(columns_path, 'rb') as file:
        fit_columns = pickle.load(file)

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
    
    X = pd.DataFrame(house_dict, index=[0])

    try:
        prediction = housingModel.predict(X)
        prediction_string = f"${prediction[0]}"
    except:
        prediction_string = ["Sorry, Not Enough Data is Available for " + neighbourhood + ". Please choose a different neighbourhood."]

   
    return jsonify(prediction_string)
    
if __name__ == "__main__":
    app.run(debug=False)