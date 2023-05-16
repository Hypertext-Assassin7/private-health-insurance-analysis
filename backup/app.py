import json
import pandas as pd
import numpy as np

# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# Flask setup
app = Flask(__name__, static_url_path='/static')

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

class client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    insurance_basic = db.Column(db.Float)
    insurance_standard = db.Column(db.Float)
    insurance_premium = db.Column(db.Float)
    insurance_option = db.Column(db.Float)

    def __repr__(self):
        return '<client %r>' % (self.name)

with app.app_context():
    db.create_all()

#################################################
# Model Setup
#################################################

from joblib import load
model_path = os.environ.get('MODEL_PATH', '') or "model_DecisionTreeRegressor.joblib"
print("Loading model...")
model = load(model_path)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact_us.html")

@app.route("/estimator", methods = ['GET','POST'])
def estimator(): 
    if request.method == 'POST':
        client_age = request.form['client_age']
        bmi = request.form['bmi']
        children_no = request.form['children_no']
        gender = request.form['gender']
        smoker = request.form['smoker']
        region = request.form['region']
        medical_history = request.form['medical_history']
        family_medical_history= request.form['family_medical_history']
        exercise_frequency = request.form['exercise_frequency']
        occupation = request.form['occupation']
        coverage_level = request.form['coverage_level']

        # get dummy data for gender
        gender_male = 1 if gender == "Male" else 0
        gender_female = 1 if gender != "Male" else 0

        # get dummy data for smoker
        smoker_no = 1 if smoker == "No" else 0
        smoker_yes = 1 if smoker != "No" else 0

        # get dummy data for region
        region_northeast = 1 if region == "Northeast" else 0
        region_northwest = 1 if region == "Northwest" else 0
        region_southeast = 1 if region == "Southeast" else 0
        region_southwest = 1 if region == "Southwest" else 0

        # get dummy date for client and family medical history
        medical_history_Diabetes = 1 if medical_history == "Diabetes" else 0
        medical_history_Heart_disease = 1 if medical_history == "Heart disease" else 0
        medical_history_High_blood_pressure = 1 if medical_history == "High blood pressure" else 0
        medical_history_None = 1 if medical_history not in ["Diabetes", "Heart disease", "High blood pressuret"] else 0

        family_medical_history_Diabetes = 1 if family_medical_history == "Diabetes" else 0
        family_medical_history_Heart_disease = 1 if family_medical_history == "Heart disease" else 0
        family_medical_history_High_blood_pressure = 1 if family_medical_history == "High blood pressure" else 0
        family_medical_history_None = 1 if family_medical_history not in ["Diabetes", "Heart disease", "High blood pressuret"] else 0

        # get dummy data for exercise_frequency
        exercise_frequency_Frequently = 1 if exercise_frequency == "Frequently" else 0
        exercise_frequency_Occasionally = 1 if exercise_frequency == "Occasionally" else 0
        exercise_frequency_Rarely = 1 if exercise_frequency == "Rarely" else 0
        exercise_frequency_Never = 1 if exercise_frequency == "Never" else 0

        # get dummy data for occupation
        occupation_Blue_collar = 1 if occupation == "Blue collar" else 0
        occupation_White_collar = 1 if occupation == "White collar" else 0
        occupation_Student = 1 if occupation == "Student" else 0
        occupation_Unemployed = 1 if occupation not in ["Blue collar", "White collar", "Student"] else 0

        # get dummy data for coverage_level
        coverage_level_Premium = 1 if coverage_level == "Premium" else 0
        coverage_level_Standard = 1 if coverage_level == "Standard" else 0
        coverage_level_Basic = 1 if coverage_level == "Basic" else 0

        client_data_list_Basic= [client_age, bmi, children_no, gender_female, gender_male, smoker_no, smoker_yes, region_northeast, region_northwest, region_southeast, region_southwest,\
                                    medical_history_Diabetes, medical_history_Heart_disease, medical_history_High_blood_pressure, medical_history_None, family_medical_history_Diabetes, \
                                    family_medical_history_Heart_disease, family_medical_history_High_blood_pressure, family_medical_history_None, exercise_frequency_Frequently, \
                                    exercise_frequency_Never, exercise_frequency_Occasionally, exercise_frequency_Rarely, occupation_Blue_collar, occupation_Student, occupation_Unemployed, \
                                    occupation_White_collar, 1, 0, 0]
        client_data_list_Premium= [client_age, bmi, children_no, gender_female, gender_male, smoker_no, smoker_yes, region_northeast, region_northwest, region_southeast, region_southwest,\
                                    medical_history_Diabetes, medical_history_Heart_disease, medical_history_High_blood_pressure, medical_history_None, family_medical_history_Diabetes, \
                                    family_medical_history_Heart_disease, family_medical_history_High_blood_pressure, family_medical_history_None, exercise_frequency_Frequently, \
                                    exercise_frequency_Never, exercise_frequency_Occasionally, exercise_frequency_Rarely, occupation_Blue_collar, occupation_Student, occupation_Unemployed, \
                                    occupation_White_collar, 0, 1, 0]
        
        client_data_list_Standard= [client_age, bmi, children_no, gender_female, gender_male, smoker_no, smoker_yes, region_northeast, region_northwest, region_southeast, region_southwest,\
                                    medical_history_Diabetes, medical_history_Heart_disease, medical_history_High_blood_pressure, medical_history_None, family_medical_history_Diabetes, \
                                    family_medical_history_Heart_disease, family_medical_history_High_blood_pressure, family_medical_history_None, exercise_frequency_Frequently, \
                                    exercise_frequency_Never, exercise_frequency_Occasionally, exercise_frequency_Rarely, occupation_Blue_collar, occupation_Student, occupation_Unemployed, \
                                    occupation_White_collar, 0, 0, 1]
        
        client_data_list_Option = [client_age, bmi, children_no, gender_female, gender_male, smoker_no, smoker_yes, region_northeast, region_northwest, region_southeast, region_southwest,\
                                    medical_history_Diabetes, medical_history_Heart_disease, medical_history_High_blood_pressure, medical_history_None, family_medical_history_Diabetes, \
                                    family_medical_history_Heart_disease, family_medical_history_High_blood_pressure, family_medical_history_None, exercise_frequency_Frequently, \
                                    exercise_frequency_Never, exercise_frequency_Occasionally, exercise_frequency_Rarely, occupation_Blue_collar, occupation_Student, occupation_Unemployed, \
                                    occupation_White_collar, coverage_level_Basic, coverage_level_Premium, coverage_level_Standard]
   
        index1 = model.predict([client_data_list_Basic])
        index2 = model.predict([client_data_list_Premium])
        index3 = model.predict([client_data_list_Standard])
        index4 = model.predict([client_data_list_Option])
        
        # response = jsonify(f"Predicted Insurance Basic: {index1}, Predicted Insurance Standard: {index2}, Predicted Insurance Premium:{index3}")

        client_insurance = client(insurance_basic=index1, insurance_premium=index2, insurance_standard=index3, insurance_option=index4)

        db.session.add(client_insurance)
        db.session.commit()

        # return jsonify(f"Predicted Insurance Basic: {index1}, Predicted Insurance Standard: {index2}, Predicted Insurance Premium:{index3}")
        return render_template("insurance_analysis.html")
    return render_template('insurance_estimator.html')

# jsonify(f"Predicted Insurance Basic: {index1}, Predicted Insurance Standard: {index2}, Predicted Insurance Premium:{index3}")

@app.route("/analysis")
def analysis():

    insurance_results = db.session.query(client.insurance_basic, client.insurance_standard, client.insurance_premium, client.insurance_option).all()

     # Create a dictionary from the row data and append to a list
    insurance_basic = [result[0] for result in insurance_results]
    insurance_standard = [result[1] for result in insurance_results]
    insurance_premium = [result[2] for result in insurance_results]
    insurance_option = [result[3] for result in insurance_results]
    data_length = len(insurance_results)-1

    insurance_data = [{'Basic': insurance_basic[data_length], 'Standard': insurance_standard[data_length], 'Premium': insurance_premium[data_length], 'Client_option': insurance_option[data_length]}]

    response = jsonify(insurance_data)
    # jsonify(f"Predicted Insurance Basic: {response[0]}, Predicted Insurance Standard: {response[1]}, Predicted Insurance Premium:{response[2]}")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
  app.run(debug=True)

