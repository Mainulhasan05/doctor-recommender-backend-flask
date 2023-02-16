from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pandas as pd
import numpy as np
import os
import sys
import xlrd
import xlwt
import openpyxl
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
doctor_data=pd.read_excel('doctor-dataset.xls')
doctor_data['Speciality']=doctor_data['Doc_Degree'].apply(lambda x: x.lower())+doctor_data['Doc_Specialist'].apply(lambda x: x.lower())+doctor_data['Speciality_Group'].apply(lambda x: x.lower())
garbage=['are','in','or','of','to','and','the','A','disease','from','a','D','B','pain','Pain','MBBS','up']
def fetch_doctor(symptoms):
    
    doctor_data['Score']=0
    for symptom in symptoms:
        for index, row in doctor_data.iterrows():
            divide=symptom.split(" ")
            for x in divide:
                if x.lower() in row['Speciality'] and x.lower() not in garbage and len(x)>2:
                    # print(x ,row['Speciality'])
                    doctor_data.at[index, 'Score'] += 1
    df_filtered = doctor_data.loc[:, doctor_data.columns != 'Speciality']
    answerList=df_filtered.sort_values(by='Score', ascending=False).values.tolist()[:5]
    
    return answerList

@app.route('/',methods=['GET','POST'])
def hello_worldaa():
    if request.method=='POST':
        symptoms_list=request.get_json()
        print(symptoms_list)
        symptoms=[]
        for x in symptoms_list:
            symptoms.append(x['name'])
        data1=fetch_doctor(symptoms)
        data=[]
        for x in data1:
            data.append(json.dumps(x, indent=2, separators=(',', ': '), ensure_ascii=False))
        # print((data))
        return {'data':list(data)}

if __name__ == '__main__':
	app.run()
# Set-ExecutionPolicy Unrestricted -Scope Process