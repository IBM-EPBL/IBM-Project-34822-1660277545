from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
from PIL import Image
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import threading
import time
import shutil
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="customer_care_registry"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""

    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_customer where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        print(myresult)
        if myresult>0:
            session['username'] = username1
            ff=open("user.txt",'w')
            ff.write(username1)
            ff.close()
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/login_admin',methods=['POST','GET'])
def login_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_login where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            #result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            msg="Your logged in fail!!!"
        

    return render_template('login_admin.html',msg=msg,act=act)

@app.route('/login_agent',methods=['POST','GET'])
def login_agent():
    cnt=0
    act=""
    msg=""

    
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM cc_agent where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('agent_home')) 
        else:
            msg="Invalid Username or Password!"
            result="Your logged in fail!!!"
        

    return render_template('login_agent.html',msg=msg,act=act)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        

        mycursor.execute("SELECT count(*) FROM cc_customer where uname=%s",(uname,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM cc_customer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO cc_customer(id,name,address,mobile,email,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,mobile,email,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
            
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='Already Exist'
            
    
    return render_template('register.html', msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    act=""
    email=""
    mess=""
    mycursor = mydb.cursor()
    

    if request.method=='POST':
        name=request.form['name']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        
        ptype=request.form['problem_type']

        

        mycursor.execute("SELECT count(*) FROM cc_agent where email=%s",(email,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
        
            mycursor.execute("SELECT max(id)+1 FROM cc_agent")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            uname="AG"+str(maxid)
            p1=randint(1000,9999)
            pass1=str(p1)
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO cc_agent(id,name,address,mobile,email,problem_type,uname,pass,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,address,mobile,email,ptype,uname,pass1,rdate)
            mycursor.execute(sql, val)
            mydb.commit()

            
            print(mycursor.rowcount, "Registered Success")
            #msg="success"
            act="1"
            mess="Dear "+name+", Agent ID: "+uname+", Password: "+pass1
            print(email)
            #if cursor.rowcount==1:
            #    return redirect(url_for('index',act='1'))
        else:
            
            msg='E-mail Already Exist!'

    
    
    return render_template('admin.html',msg=msg,email=email,mess=mess,act=act)

@app.route('/view_agent', methods=['GET', 'POST'])
def view_agent():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cc_agent where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_agent')) 
        
    return render_template('view_agent.html',data=data,act=act)

@app.route('/view_customer', methods=['GET', 'POST'])
def view_customer():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer")
    data = mycursor.fetchall()
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from cc_customer where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_customer')) 
        
    return render_template('view_customer.html',data=data,act=act)


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname, ))
    data = mycursor.fetchone()

    
    return render_template('userhome.html',data=data,act=act)



@app.route('/cus_img', methods=['GET', 'POST'])
def cus_img():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]
    aid=data[0]

    if request.method=='POST':
        
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            photo="C"+str(aid)+filename
            file.save(os.path.join("static/upload", photo))
            mycursor.execute("update cc_customer set photo=%s where uname=%s",(photo,uname))
            mydb.commit()
            msg="success"
        
    return render_template('cus_img.html',data=data,msg=msg)


@app.route('/cus_pass', methods=['GET', 'POST'])
def cus_pass():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]

    if request.method=='POST':
        oldpass=request.form['oldpass']
        newpass=request.form['newpass']

        mycursor.execute("SELECT count(*) FROM cc_customer where uname=%s && pass=%s",(uname,oldpass))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            mycursor.execute("update cc_customer set pass=%s where uname=%s",(newpass,uname))
            mydb.commit()
            msg="success"
        else:
            msg="wrong"
            

        
    return render_template('cus_pass.html',data=data,msg=msg)



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
