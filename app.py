import urllib.request,json
import requests
import sqlite3
import json
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder='templates', static_folder='static')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

# Enter your database connection details below


# Intialize MySQL
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age=db.Column(db.Integer,nullable=False )
    sex=db.Column(db.String(10), nullable=False)
    comp=db.Column(db.String(100))
     
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.age}', '{self.sex}','{self.comp}', )"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dept=db.Column(db.String(100))
     
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.dept}', )"



@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/contact/')
def contact():
    return render_template('contact.html')

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/userlogin/', methods=['GET', 'POST'])
def Userlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        user = User.query.filter_by(username=username).first() 
        # Fetch one record and return result
        # If account exists in account table in out database
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username
            # Redirect to home page
            return redirect(url_for('account'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Userlogin.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('about'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/Uregister', methods=['GET', 'POST'])
def Uregister():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age=request.form['age']
        sex=request.form['sex']
        comp=request.form['comp']
                # Check if account exists using MySQL
        account=User.query.filter_by(email=email).first()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into account table
            user = User(username=username ,email=email, password=password,age=age,sex=sex,comp=comp)
            db.session.add(user)
            db.session.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('Uregister.html', msg=msg)

@app.route("/account")
def account():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        user = User.query.filter_by(id=session['id']).first() 
       
        if user.id == 1:
            address="https://api.thingspeak.com/channels/1376240/feeds.json?api_key=ZIM3I3G3P3UUCLYV&results=1"
        elif user.id ==2:
            address="https://api.thingspeak.com/channels/1376244/feeds.json?api_key=ZB68KBX54MV7LRD8&results=1"
        elif user.id ==3:
            address="https://api.thingspeak.com/channels/1376245/feeds.json?api_key=RS5I07VIQ8LWZPJ7&results=1"
        elif user.id ==4:
            address="https://api.thingspeak.com/channels/1376246/feeds.json?api_key=H5WC6QGEL44H566T&results=1"
        else:
            address="https://api.thingspeak.com/channels/1376244/feeds.json?api_key=ZB68KBX54MV7LRD8&results=2"
        
        
        conn  = urllib.request.urlopen(address)
        response = conn.read()
        #print ("http status code=%s" % (conn.getcode()))
        data=json.loads(response)
        age=20
        sex="F"
        temp=[]
        heart=[]
        spo2=[]
        pers=[]
        ecg=[]
        arr5=[]
        for d in data['feeds']:
            temp="{0:.{1}f}".format(float(d['field3']),2)
            heart="{0:.{1}f}".format(float(d['field4']),2)
            spo2="{0:.{1}f}".format(float(d['field5']),2)
            pers="{0:.{1}f}".format(float(d['field6']),2)
            ecg="{0:.{1}f}".format(float(d['field7']),2)
            arr5="{0}".format(d['created_at'])
        conn.close()

        
        
        return render_template("main.html", Temperature=temp, BloodOxygen=spo2,HeartRate=heart, time=arr5, account=user, age=age,sex=sex,pers=pers,ecg=ecg)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('Userlogin'))

@app.route('/Doctorlogin/', methods=['GET', 'POST'])
def Doctorlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        doctor = Doctor.query.filter_by(username=username).first() 
        # Fetch one record and return result
        # If account exists in account table in out database
        if doctor:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = doctor.id
            session['username'] = doctor.username
            # Redirect to home page
            return redirect(url_for('Daccount'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Doctorlogin.html', msg=msg)

@app.route('/Dregister', methods=['GET', 'POST'])
def Dregister():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'dept' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        dept=request.form['dept']
                # Check if account exists using MySQL
        account=Doctor.query.filter_by(email=email).first()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into account table
            doctor = Doctor(username=username, email=email, password=password,dept=dept)
            db.session.add(doctor)
            db.session.commit()
            msg = 'doctor has successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('Dregister.html', msg=msg)

@app.route("/data1")
def data1():
    return render_template("data1.html")

@app.route("/data2")
def data2():
    return render_template("data2.html")

@app.route("/data3")
def data3():
    return render_template("data3.html")

@app.route("/data4")
def data4():
    return render_template("data4.html")

@app.route("/sensor_feed")
def sensor_feed():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        user = User.query.filter_by(id=session['id']).first() 
       
        if user.id == 1:
            return render_template("graphs1.html")
            
        elif user.id ==2:
            return render_template("graphs2.html")
            
        elif user.id ==3:
            return render_template("graphs3.html")
            
        else:
            return render_template("snesor_feed.html")
            
        
        
        
    
    # User is not loggedin redirect to login page
    return redirect(url_for('Userlogin'))

    
  



@app.route("/Daccount")
def Daccount():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        doctor = Doctor.query.filter_by(id=session['id']).first() 
        user1 = User.query.filter_by(id=1).first() 
        user2= User.query.filter_by(id=2).first() 
        user3 = User.query.filter_by(id=3).first()
        user4 = User.query.filter_by(id=4).first() 

        

        a1="https://api.thingspeak.com/channels/1376240/feeds.json?api_key=ZIM3I3G3P3UUCLYV&results=1"
        a2="https://api.thingspeak.com/channels/1376244/feeds.json?api_key=ZB68KBX54MV7LRD8&results=1"
        a3="https://api.thingspeak.com/channels/1376245/feeds.json?api_key=RS5I07VIQ8LWZPJ7&results=1"
        a4="https://api.thingspeak.com/channels/1376246/feeds.json?api_key=H5WC6QGEL44H566T&results=1" 
        a=[a1,a2,a3,a4]
        conn  = urllib.request.urlopen(a1)
        response = conn.read()
        data=json.loads(response)
        #print ("http status code=%s" % (conn.getcode()))
        temp=[]
        heart=[]
        spo2=[]
        pers=[]
        ecg=[]
        arr5=[]
        for d in data['feeds']:
            temp="{0:.{1}f}".format(float(d['field3']),2)
            heart="{0:.{1}f}".format(float(d['field4']),2)
            spo2="{0:.{1}f}".format(float(d['field5']),2)
            pers="{0:.{1}f}".format(float(d['field6']),2)
            ecg="{0:.{1}f}".format(float(d['field7']),2)
            arr5="{0}".format(d['created_at'])
        conn.close()
        p=[temp,heart,spo2,pers,ecg,arr5]
        #2nd
        conn  = urllib.request.urlopen(a2)
        response = conn.read()
        data=json.loads(response)
        #print ("http status code=%s" % (conn.getcode()))
        temp1=[]
        heart1=[]
        spo21=[]
        pers1=[]
        ecg1=[]
        arr51=[]
        for d in data['feeds']:
            temp1="{0:.{1}f}".format(float(d['field3']),2)
            heart1="{0:.{1}f}".format(float(d['field4']),2)
            spo21="{0:.{1}f}".format(float(d['field5']),2)
            pers1="{0:.{1}f}".format(float(d['field6']),2)
            ecg1="{0:.{1}f}".format(float(d['field7']),2)
            arr51="{0}".format(d['created_at'])
        conn.close()
        p1=[temp1,heart1,spo21,pers1,ecg1,arr51]



        #3rd
        conn  = urllib.request.urlopen(a3)
        response = conn.read()
        data=json.loads(response)
        #print ("http status code=%s" % (conn.getcode()))
        temp2=[]
        heart2=[]
        spo22=[]
        pers2=[]
        ecg2=[]
        arr52=[]
        for d in data['feeds']:
            temp2="{0:.{1}f}".format(float(d['field3']),2)
            heart2="{0:.{1}f}".format(float(d['field4']),2)
            spo22="{0:.{1}f}".format(float(d['field5']),2)
            pers2="{0:.{1}f}".format(float(d['field6']),2)
            ecg2="{0:.{1}f}".format(float(d['field7']),2)
            arr52="{0}".format(d['created_at'])
        conn.close()
        p2=[temp2,heart2,spo22,pers2,ecg2,arr52]
        



        return render_template("Daccount.html",account=doctor,array=a,data=[p,p1,p2],user1=user1,user2=user2,user3=user3,graphs="graphs4")
    
    # User is not loggedin redirect to login page
    return redirect(url_for('Doctorlogin'))

@app.route('/plots/graphs')
def graphs():
    return render_template("plots/graphs.html")


if __name__ == "__main__":
    app.run(debug=True)
