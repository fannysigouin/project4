from flask import Flask, render_template, jsonify, request
from flask import Markup
import requests
import sqlalchemy
from sqlalchemy import create_engine, text
import psycopg2
import pickle
import pandas as pd


#################################################
# Flask Setup
#################################################
app = Flask(__name__, template_folder='templates')

@app.route("/")
def homepage():
    return render_template('home.html') 


@app.route("/get_neighbourhoods")
def get_neighbourhoods():
    engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/listings_db')
    query = text("SELECT distinct neighbourhood FROM toronto_listings")
    data = engine.execute(query)
    return data

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

    pkl_scaler = "housingScaler.pkl"  
    with open(pkl_scaler, 'rb') as file:  
        housingScaler = pickle.load(file)

    neighbourhood_key = "neighbourhood_" + neighbourhood
    property_type_key = "property_type_" + property_type

    house_dict = {"beds": beds,
                  "baths": baths,
                  "dens": dens,
                  neighbourhood_key: neighbourhood,
                  property_type_key: property_type}
    
    X = pd.DataFrame(house_dict)

    X_scaled = housingScaler.transform(X)
    
    prediction = housingModel.predict(X_scaled)

    return prediction
    
if __name__ == "__main__":
    app.run(debug=False)