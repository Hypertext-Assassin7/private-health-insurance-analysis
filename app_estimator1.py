""" This is an example of a flask application called 'Iris'
with both UI and API components
"""

# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
# 'or' allows us to later switch from 'sqlite' to an external database like 'postgres' easily
# os.environ is used to access 'environment variables' from the operating system
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# TODO: Add data models if needed

with app.app_context():
    db.create_all()

#################################################
# Model Setup
#################################################

from joblib import load
model_path = os.environ.get('MODEL_PATH', '') or "model_LinearRegression.joblib"
print("Loading model...")
model = load(model_path)

#################################################
# Web User Interface - Front End
#################################################
# note that UI routes return a html response
# you can add as many html pages as you need
# below is an example to get you started...

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("insurance_estimator1.html")

# TODO: Add more routes if needed

#################################################
# API - Back End
#################################################
# we will use '/api/..' for our api within flask application
# note that api returns a JSON response
# you can add as many API routes as you need
# below is an example to get you started...

@app.route("/score", methods=["POST"])
def predict():
    #return 'test2 message'
 
    
    index1 = model.predict([[46,21.45,5,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0]])
    index2 = model.predict([[22,32.13,5,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0]])
    #return jsonify(f"{client_age}, {gender}, {bmi}")
    return jsonify(f"Predicted Insurance Premium1: {index1} and Predicted Insurance Premium2: {index2}  ")

if __name__ == "__main__":

    # run the flask app
    app.run()
