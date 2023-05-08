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

    estimate.append(client_age)
    estimate.append(bmi)
    estimate.append(children_no)

    lgender = ["male", "female"]
    lsmoker = ["no", "yes"]
    lregion = ["northeast", "northwest", "southeast", "southwest"]
    lmedical_history = ["Diabetes", "Heart disease", "High blood pressure", "None"]
    lfamily_medical_history = ["Diabetes", "Heart disease", "High blood pressure", "None"]
    lexercise_frequency = ["Frequently", "Never", "Occasionally", "Rarely"]
    loccupation = ["Blue collar", "Student", "Unemployed", "White collar"]
    lcoverage_level = ["Basic", "Premium", "Standard"]



    gendum = []
    gensmoke = []
    genreg =[]
    genmed = []
    genfam = []
    genexe = []
    genocc = []
    gencov = []


    for i in range(len(lgender)):
        gendum.append(0)
    for i in range(len(lgender)):
        if lgender[i] == gender:
            gendum[i]=1
    estimate.extend(gendum)    
 
    for i in range(len(lsmoker)):
        gensmoke.append(0)
    for i in range(len(lsmoker)):
        if lsmoker[i] == smoker:
            gensmoke[i]=1
    estimate.extend(gensmoke)
       
               
    for i in range(len(lmedical_history)):
        genmed.append(0)
    for i in range(len(lmedical_history)):
        if lmedical_history[i] == medical_history:
            genmed[i]=1
    estimate.extend(genmed)
                
    for i in range(len(lfamily_medical_history)):
        genfam.append(0)
    for i in range(len(lfamily_medical_history)):
        if lfamily_medical_history[i] == family_medical_history:
            genfam[i]=1
    estimate.extend(genfam)
                    
    for i in range(len(lexercise_frequency)):
        genexe.append(0)
    for i in range(len(lexercise_frequency)):
        if lexercise_frequency[i] == exercise_frequency:
            genexe[i]=1
    estimate.extend(genexe)
                    
    for i in range(len(loccupation)):
        genocc.append(0)
    for i in range(len(loccupation)):
        if loccupation[i] == occupation:
            genocc[i]=1
    estimate.extend(genocc)
                    
    for i in range(len(lcoverage_level)):
        gencov.append(0)
    for i in range(len(lcoverage_level)):
        if lcoverage_level[i] == coverage_level:
            gencov[i]=1
    estimate.extend(gencov)
        


    index1 = model.predict([estimate])






    return jsonify(f"estimate data: {estimate}, Predicted Insurance Premium1: {index1}") 
    
    client_data = {
        "age": client_age,
        "gender": gender,
        "bmi": bmi,
        "children": children_no,
        'smoker': smoker,
        'medical_history': medical_history,
        'family_medical_history': family_medical_history,
        'exercise_frequency': exercise_frequency,
        'occupation': occupation,
        'coverage_level': coverage_level
    } 


    json_string = json.dumps(client_data)
    print(json_string)

    return json_string

   
if __name__ == '__main__':
  app.run()