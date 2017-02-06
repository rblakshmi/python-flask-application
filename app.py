# -*- coding: utf-8 -*-
# R.B.Laskhmi web application 
# for breastcancer
from flask import Flask, render_template, url_for,request,flash,redirect
from wtforms import validators,TextField,SubmitField,IntegerField,SelectField,RadioField,TextAreaField
from flask_wtf import Form
import sqlite3
import pandas as pd
import pickle
import os



app = Flask(__name__)
app.secret_key = 'developement'

class DocLogin(Form):
    d_id = IntegerField("ID",[validators.DataRequired() ])
    d_name = TextField("Name", [validators.DataRequired() ])
    d_submit = SubmitField("send")

class PatientLogin(Form):
    id = IntegerField("ID",[validators.DataRequired() ])
    name = TextField("Name", [validators.DataRequired() ])
    submit = SubmitField("send")

class PatientDetail(Form):
    id = IntegerField("Patient ID",[validators.DataRequired() ])
    name = TextField("Patient Name", [validators.DataRequired() ])
    age = IntegerField("Patient Age")
    

def validate_patient(form):
    username = form.name.data
    password = form.id.data
    data = connect_patient()
    recordset = data[data.name == username]
    if recordset.empty == False:
        if password == recordset.id.item():
            return True
        else:
            return False
    else:
        return False 

    
class DiagnosticDetail(Form):
    id = IntegerField("Patient ID",[validators.DataRequired() ])
    name = TextField("Patient Name", [validators.DataRequired() ])
    age = IntegerField("Patient Age")
    clumpthickness= IntegerField("CLUMP THICKNESS",[validators.DataRequired() ])
    size_uniformity= IntegerField("SIZE UNIFORMITY",[validators.DataRequired() ])
    shape_uniformity = IntegerField("SHAPE UNIFORMITY",[validators.DataRequired() ])
    marginal_adhesion = IntegerField(" MARGINAL ADHESION",[validators.DataRequired() ])
    epithelial_size = IntegerField("EPITHELIAL SIZE",[validators.DataRequired() ])
    bare_nuclei = IntegerField("BARE NUCLEI",[validators.DataRequired() ])
    bland_cromatin = IntegerField("BLAND CROMATIN",[validators.DataRequired() ])
    normal_nuclei = IntegerField("NORMAL NUCLEI",[validators.DataRequired() ])
    mitosis = IntegerField("MITOSIS",[validators.DataRequired() ])
    predict = SubmitField("predict") 

def connect_patient():
    conn = sqlite3.connect('patient.sqlite')
    c = conn.cursor()
    users = c.execute("SELECT * FROM patient_db")
    data = users.fetchall()
    dataframe = pd.DataFrame(data , columns =['id' , 'name', 'age', 'class'])
    print("success")
    conn.commit()
    c.close()
    conn.close()
    return dataframe


def model(form2):
    df = pd.DataFrame([[form2.clumpthickness.data , 
                        form2.size_uniformity.data , 
                        form2.shape_uniformity.data , 
                        form2.marginal_adhesion.data , 
                        form2.epithelial_size.data , 
                        form2.bare_nuclei.data , 
                        form2.bland_cromatin.data , 
                        form2.normal_nuclei.data , 
                        form2.mitosis.data]],
                        columns = ['clumpthickness','size_uniformity','shape_uniformity','marginal_adhesion','epithelial_size','bare_nuclei','bland cromatin','normal_nuclei' , 'mitosis'])
    #deserialise the model
    cur_dir = os.path.dirname(__file__)
    stop = pickle.load(open(os.path.join(cur_dir,'model.pkl'), 'rb'))
    res = stop.predict(df)
    if(res == [2]):
        result = "benign"
    elif(res == [4]):
        result = "malignant"
    return result
    

def connect_doctor():
    conn = sqlite3.connect('patient.sqlite')
    c = conn.cursor()
    users = c.execute("SELECT * FROM doctor_db")
    data = users.fetchall()
    dataframe = pd.DataFrame(data , columns =['id' , 'name'])
    conn.commit()
    conn.close()
    return dataframe

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/patient', methods = ['GET', 'POST'])
def contact():
   form = PatientLogin()
   if request.method == 'POST':
      if form.validate():
          username = form.name.data
          password = form.id.data
          data = connect_patient()
          recordset = data[data.name == username]
          if recordset.empty == False:
              if password == recordset.id.item():
                  return render_template('patient_table.html' , recordset = recordset)
              else:
                  return redirect(url_for('welcome'))
          else:
              return redirect(url_for('welcome'))
      else:
          flash('all fields are required')
          return render_template('patient.html' , form=form)
   elif request.method == 'GET':
         return render_template('patient.html', form = form)
        
@app.route('/doctor', methods = ['GET', 'POST'])
def doc():
   form = DocLogin()
   
   if request.method == 'POST':
      if form.validate() == True:
          username = form.d_name.data
          password = form.d_id.data
          data = connect_doctor()
          recordset = data[data.name == username] 
          #form1 = PatientDetail()
          form2 = DiagnosticDetail()
          if recordset.empty == False:
              if password == recordset.id.item():
                  return render_template('patient_detail.html',form2=form2)
              else:
                  flash("password id invalid")
                  return render_template('doctor.html', form = form)
          else:
              flash("invalid username")
              return render_template('doctor.html', form = form)
      else:
          flash('All fields are required.')
          return render_template('doctor.html', form = form)
   elif request.method == 'GET':
         return render_template('doctor.html', form = form)

@app.route('/doctor/pdetails' , methods = ['GET','POST'])
def DocPatient():
    #form = PatientDetail()
    form1 = DiagnosticDetail()
    if request.method == 'POST':
        if form1.validate():
            op = validate_patient(form1)
            if op == True:
                res = model(form1)
                conn = sqlite3.connect('patient.sqlite')
                c = conn.cursor()
                c.execute("UPDATE patient_db SET CLASS = ? WHERE NAME = ?",(res,form1.name.data))
                conn.commit()
                c.close()
                conn.close()
                return render_template('success.html',res=res)
            else:
                flash("invalid patient detail")
                return render_template('welcome.html')
        else:
            flash("enter all the detail")
            return render_template('welcome.html')
    elif request.method == 'GET':
        return render_template('patient_detail.html', form2 = form1)
  

        
@app.route('/doctor/pdetails/padd' , methods = ['GET','POST'])
def padd():
   #form = PatientDetail()
   form = DiagnosticDetail()
   if request.method == 'POST':
      if form.validate() == True:
         username = form.name.data
         password = form.id.data
         age = form.age.data
         conn = sqlite3.connect('patient.sqlite')
         c = conn.cursor()
         c.execute('INSERT INTO patient_db VALUES(?,?,?,?)',(password,username,age,""))
         conn.commit()
         c.close()
         conn.close()
         flash("patient added")
         res = model(form)
         conn = sqlite3.connect('patient.sqlite')
         c = conn.cursor()
         c.execute("UPDATE patient_db SET CLASS = ? WHERE NAME = ?",(res,form.name.data))
         conn.commit()
         c.close()
         conn.close()
         #form2 = DiagnosticDetail()
         return render_template('success.html',res=res)
      else:
          flash("all fields are required")
          return render_template('add_patient.html', form2 = form)
   elif request.method == 'GET':
         return render_template('add_patient.html',form2 = form)

if __name__  == '__main__':
    app.run(debug=True,)
