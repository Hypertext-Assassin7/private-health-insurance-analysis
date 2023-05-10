import json
import pandas as pd
import os
from flask import Flask, request, jsonify, render_template, session


# Flask setup
app = Flask(__name__)

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


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("insurance_estimator.html")

@app.route("/estimator", methods = ['POST'])
def estimator(): 
    estimate = []
    
    #create library of all categories
    library = {'gender': ['male', 'female'], 'smoker': ['yes', 'no'], 'region': ['southeast', 'northwest', 'southwest', 'northeast'], 'medical_history': ['Diabetes', 'None', 'High blood pressure', 'Heart disease'], 'family_medical_history': ['None', 'High blood pressure', 'Diabetes', 'Heart disease'], 'exercise_frequency': ['Never', 'Occasionally', 'Rarely', 'Frequently'], 'occupation': ['Blue collar', 'White collar', 'Student', 'Unemployed'], 'coverage_level': ['Premium', 'Standard', 'Basic']}
    #identify  the original column headers (also in library - used for lookup
    column = ['gender','smoker', 'region', 'medical_history', 'family_medical_history', 'exercise_frequency', 'occupation', 'coverage_level']
    
    #retrieve dta from html form
    client_age = request.form['client_age']
    bmi = request.form['bmi']
    children_no = request.form['children_no']
    gender = request.form['gender']
    smoker = request.form['smoker']
    medical_history = request.form['medical_history']
    family_medical_history= request.form['family_medical_history']
    exercise_frequency = request.form['exercise_frequency']
    occupation = request.form['occupation']
    coverage_level = request.form['coverage_level']
    
    #Create a list of categorical form answers
    form_input = [gender, smoker, medical_history, family_medical_history, exercise_frequency, occupation, coverage_level]
    
    #enter  numerical values for prediction
    estimate.append(client_age)
    estimate.append(bmi)
    estimate.append(children_no)
    
    #create numerical values for categories for prediction
    for j in range(len(column)):
        item = column[j]
        temp = []
        for i in range(len(library[item])):
            temp.append(0)
            if library[item][i] == form_input[2]:
                temp[i] = 1
        estimate.extend(temp)
 


    return jsonify(f"estimate data: {estimate}, Predicted Insurance Premium1: ") 
    

   
if __name__ == '__main__':
  app.run()