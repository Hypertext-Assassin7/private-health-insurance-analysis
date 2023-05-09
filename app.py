import json
import pandas as pd

from flask_session import Session

# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# Flask setup
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

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return '<Pet %r>' % (self.name)

with app.app_context():
    db.create_all()

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("insurance_estimator.html")

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

      client_data = {
          "age": client_age,
          "bmi": bmi,
          "children": children_no,
          "gender_female": gender_female,
          "gender_male": gender_male,
          'smoker_no': smoker_no,
          'smoker_yes': smoker_yes,
          'region_northeast': region_northeast,
          'region_northwest': region_northwest,
          'region_southeast': region_southeast,
          'region_southwest': region_southwest,
          'medical_history_Diabetes' : medical_history_Diabetes,
          'medical_history_Heart_disease': medical_history_Heart_disease,
          'medical_history_High_blood_pressure': medical_history_High_blood_pressure,
          'medical_history_None' : medical_history_None,
          'family_medical_history_Diabetes' : family_medical_history_Diabetes,
          'family_medical_history_Heart_disease': family_medical_history_Heart_disease,
          'family_medical_history_High_blood_pressure': family_medical_history_High_blood_pressure,
          'family_medical_history_None' : family_medical_history_None,
          'exercise_frequency_Frequently': exercise_frequency_Frequently,
          'exercise_frequency_Never': exercise_frequency_Never,
          'exercise_frequency_Occasionally': exercise_frequency_Occasionally,
          'exercise_frequency_Rarely': exercise_frequency_Rarely,
          'occupation_Blue_collar': occupation_Blue_collar,
          'occupation_Student': occupation_Student,
          'occupation_Unemployed': occupation_Unemployed,
          'occupation_White_collar': occupation_White_collar,
          'coverage_level_Premium': coverage_level_Premium,
          'coverage_level_Standard': coverage_level_Standard,
          'coverage_level_Basic': coverage_level_Basic
      }
    
      json_string = json.dumps(client_data)
      print(json_string)

      # data = client_data_db(age=client_age, gender=gender, bmi=bmi, children=children_no, smoker=smoker, medical_history=medical_history,family_medical_history=family_medical_history, exercise_frequency=exercise_frequency, occupation=occupation, coverage_level=coverage_level)

      # pet = client_data_db(age=client_age, gender=lat, lon=lon)
      # db.session.add(pet)
      # db.session.commit()

      return json_string
    return render_template("insurance_estimator.html")

if __name__ == '__main__':
  app.run(debug=True)

