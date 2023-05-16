# The purpose of this project is to:
   - develop a machine learning model for a data set containing insurance premiums based on 3 numerical and 8 categorical data 
   - utilize the model to predict insurance premium cost for customers
   - develop a company website that offers a page that enables customers to predict the insurance premiums based on their personal conditions.
   - Provide data analysis on the submitted and predicted data, that provides useful information for business planning and marketing.

## Data set
A data set from Kaggle was used for the source of our analysis: Insurance Data for Machine Learning | Kaggle

## Machine Learning Model development: insurance_ml.ipynb
   ### insurance_ml.ipynb was developed to
        ●	read the data set (csv file)
            ○	Features
                ■	Numerical data
                    ●	age 
                    ●	bmi 
                    ●	children 
                ■	Categorical data
                    ●	gender 
                    ●	smoker 
                    ●	region 
                    ●	medical_history 
                    ●	family_medical_history 
                    ●	exercise_frequency 
                    ●	occupation 
                    ●	coverage_level 
            ○	Target      
                ■	charges 
        ●	Utilise OneHotEncoder to create a file that can be used for training and testing the models.
        ●	Linear regression and Decison Tree regression was usedfor our modelling. provided very high accuracy
 
## Web application framework: app.py
app.py is a python flask file used to interface between the company web site, prediction calculation, capturing the user supplied data in a sqlite database and recalling the supplied data for business planning analysis.
Once app.py is started open http://127.0.0.1:5000 to access the landing page, index.html.
 
## Web pages
All html files are located in the /templates folder. Each page is called by the hyperlink on each page and their respective code in app.py.
Index.html : Main page
insurance_estimator.html: data entry form (Quote)
Insurance_analysis.html: Insurance premium Prediction
Internal_analysis.html: analysis of sqlite data (user supplied information)
password.html: password protection for internal analysis
Cover_options.html: summary of covers provided
Contact_us.html: contacts page
About.html: about

## static folder
The static folder contains files referenced by the html files. These include images, js and files.

## Sqlite database
The user supplied data and associated predictions are included in the /instance folder.
Each data submission on the quotation page, will be recorded here.

## Additional Data Analysis
Private_health_analysis.ipynb was used to  analyse the data source. It is assumed that the data was fabricated or at least  modified as all data a options seem to  result in equal amounts. E.g. male/female, smoker/non smoker, regions etc. 

