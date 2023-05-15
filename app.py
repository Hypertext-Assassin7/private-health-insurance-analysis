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
    redirect,
    url_for)

# Flask setup
app = Flask(__name__, static_url_path='/static')

#################################################
# Database Setup
#################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# 'or' allows us to later switch from 'sqlite' to an external database like 'postgres' easily
# os.environ is used to access 'environment variables' from the operating system
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    insurance_age = db.Column(db.Integer)
    insurance_bmi = db.Column(db.Integer)
    insurance_children_no = db.Column(db.Integer)
    insurance_gender = db.Column(db.String(20))
    insurance_smoker = db.Column(db.String(20))
    insurance_region = db.Column(db.String(20))
    insurance_medical_history = db.Column(db.String(20))
    insurance_family_medical_history = db.Column(db.String(20))
    insurance_exercise_frequency = db.Column(db.String(20))
    insurance_occupation = db.Column(db.String(20))
    insurance_coverage_level = db.Column(db.String(20))
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

@app.route("/cover_options")
def cover_option():
    return render_template("cover_options.html")

@app.route("/estimator", methods = ['GET','POST'])
def estimator(): 
    if request.method == 'POST':
        estimate = []

        #Create a list of categorical form answers that will be entered into estimate/prediction
        library = {'gender': ['Female', 'Male'], 'smoker': ['No', 'Yes'], 'region': ['Northeast', 'Northwest','Southeast', 'Southwest'], 'medical_history': ['Diabetes', 'Heart disease', 'High blood pressure', 'None'], 'family_medical_history': ['Diabetes', 'Heart disease', 'High blood pressure', 'None'], 'exercise_frequency': ['Frequently', 'Never', 'Occasionally', 'Rarely'], 'occupation': ['Blue collar', 'Student', 'Unemployed', 'White collar'], 'coverage_level': ['Basic', 'Premium', 'Standard']}
        #identify  the original column headers (also in library - used for lookup
        column = ['gender','smoker', 'region', 'medical_history', 'family_medical_history', 'exercise_frequency', 'occupation', 'coverage_level']
    
        #retrieve data from html form
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
        
        #Create a list of categorical form answers
        form_input = [gender, smoker, region, medical_history, family_medical_history, exercise_frequency, occupation, coverage_level]
        
        #enter numerical values for estimate/prediction
        estimate.append(client_age)
        estimate.append(bmi)
        estimate.append(children_no)
        
        #create numerical values (get_dummies) for categories for estimate/prediction
        for j in range(len(column)):
            item = column[j]
            temp = []
            for selection in range(len(library[item])):
                temp.append(0)
            for i in range(len(library[item])):
                if library[item][i] == form_input[j]:
                    temp[i] = 1
            estimate.extend(temp)
        
        # Create corrections for all 3 price options and customer chosen option
        client_data_list_Basic=estimate.copy()
        client_data_list_Basic[27:30]=[1, 0, 0]
            
        client_data_list_Standard=estimate.copy()
        client_data_list_Standard[27:30]=[0, 0, 1]
            
        client_data_list_Premium=estimate.copy()
        client_data_list_Premium[27:30]=[0, 1, 0]
            
        client_data_list_Option=estimate.copy()
        
        # Establish predicted fees using model        
        index1 = model.predict([client_data_list_Basic])
        index2 = model.predict([client_data_list_Standard])
        index3 = model.predict([client_data_list_Premium])
        index4 = model.predict([client_data_list_Option])
        
        # response = jsonify(f"Predicted Insurance Basic: {index1}, Predicted Insurance Standard: {index2}, Predicted Insurance Premium:{index3}")
        
        #Establish data to be uploaded into sqlite DB
        client_insurance = client(insurance_age = client_age, insurance_bmi = bmi, insurance_children_no = children_no, insurance_gender = gender, insurance_smoker = smoker, insurance_region = region, insurance_medical_history = medical_history, insurance_family_medical_history = family_medical_history, insurance_exercise_frequency = exercise_frequency, insurance_occupation = occupation, insurance_coverage_level = coverage_level, insurance_basic=index1, insurance_standard=index2, insurance_premium=index3, insurance_option=index4)

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

    #Identify last row of data
    insurance_data = [{'Basic': insurance_basic[data_length], 'Standard': insurance_standard[data_length], 'Premium': insurance_premium[data_length], 'Client_option': insurance_option[data_length]}]
    response = jsonify(insurance_data)

    # jsonify(f"Predicted Insurance Basic: {response[0]}, Predicted Insurance Standard: {response[1]}, Predicted Insurance Premium:{response[2]}")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/analytics")
def analytics():
    
    # group by and count features and ready for xValue and yValue to do plots
    regions = db.session.query(client.insurance_region, func.count(client.insurance_region)).group_by(client.insurance_region).all()
    excercise = db.session.query(client.insurance_exercise_frequency, func.count(client.insurance_exercise_frequency)).group_by(client.insurance_exercise_frequency).all()
    smoker = db.session.query(client.insurance_smoker, func.count(client.insurance_smoker)).group_by(client.insurance_gender, client.insurance_smoker).all()
    occupation = db.session.query(client.insurance_occupation, func.count(client.insurance_occupation)).group_by(client.insurance_gender, client.insurance_occupation).all()
    # medical = db.session.query(client.insurance_medical_history, func.count(client.insurance_medical_history)).groupy_by(client.insurance_medical_history).all()
    # family_medical = db.session.query(client.insurance_family_medical_history, func.count(client.insurance_family_medical_history)).groupy_by(client.insurance_family_medical_history).all()

    medical = db.session.query(client.insurance_medical_history, func.count(client.insurance_medical_history)).group_by(client.insurance_medical_history).all()
    family_medical = db.session.query(client.insurance_family_medical_history, func.count(client.insurance_family_medical_history)).group_by(client.insurance_family_medical_history).all()

    reg_ana_x = [result[0] for result in regions]
    reg_ana_y = [result[1] for result in regions]

    exe_ana_x = [result[0] for result in excercise]
    exe_count_y = [result[1] for result in excercise]

    smoker_x = [result[0] for result in smoker]
    smoker_y = [result[1] for result in smoker]

    occupation_x = [result[0] for result in occupation]
    occupation_y = [result[1] for result in occupation]

    medical_x = [result[0] for result in medical]
    medical_y = [result[1] for result in medical]

    family_medical_x = [result[0] for result in family_medical]
    family_medical_y = [result[1] for result in family_medical]

    reg_ana_list = [{'regions': reg_ana_x}, {"count": reg_ana_y}, {'exercise': exe_ana_x}, {'exe_count':exe_count_y}, {'smoker': smoker_x}, {'smoker_count': smoker_y}, {'occupation': occupation_x}, {'occupation_count': occupation_y}, {'medical_history': medical_x}, {'medical_count': medical_y}, {'family_medical_history': family_medical_x}, {'family_medical_count': family_medical_y}]
    response_reg = jsonify(reg_ana_list)

    response_reg.headers.add('Access-Control-Allow-Origin', '*')

    return response_reg

@app.route("/management")
def management():
    return render_template("internal_analysis.html")

@app.route("/password")
def password():
    return render_template("password.html")

if __name__ == '__main__':
  app.run(debug = True)
  