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

@app.route('/cus_send', methods=['GET', 'POST'])
def cus_send():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        sw_name=request.form['sw_name']
        sw_link=request.form['sw_link']
        details=request.form['details']
               
        ptype=request.form['problem_type']

      
        
        mycursor.execute("SELECT max(id)+1 FROM cc_token")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        mycursor.execute("SELECT * FROM cc_agent where problem_type=%s order by rand()",(ptype, ))
        data1 = mycursor.fetchall()
        x=1
        for rr in data1:
            if x==1:
                agent=rr[6]
            x+=1
        
        sql = "INSERT INTO cc_token(id,uname,sw_name,sw_link,problem_type,details,agent,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,sw_name,sw_link,ptype,details,agent,rdate)
        print(sql)
        print(val)
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        act="1"
        
        #if cursor.rowcount==1:
        #    return redirect(url_for('index',act='1'))
   

    
    
    return render_template('cus_send.html',data=data,act=act)

@app.route('/test1', methods=['GET', 'POST'])
def test1():

    return render_template('test1.html')
    
@app.route('/cus_send1', methods=['GET', 'POST'])
def cus_send1():
    act=""
    uname=""
    agent=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        sw_name=request.form['sw_name']
        sw_link=request.form['sw_link']
        details=request.form['details']
               
        ptype=request.form['problem_type']
        mycursor.execute("SELECT max(id)+1 FROM cc_token")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        mycursor.execute("SELECT * FROM cc_agent where problem_type=%s order by rand()",(ptype, ))
        data1 = mycursor.fetchall()
        x=1
        for rr in data1:
            if x==1:
                agent=rr[6]
            x+=1
    
        #agent="a"
        #data1[6]

        sql = "INSERT INTO cc_token(id,uname,sw_name,sw_link,problem_type,details,agent,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,sw_name,sw_link,ptype,details,agent,rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        act="1"

    return render_template('cus_send.html',data=data,act=act)

    


@app.route('/cus_feedback', methods=['GET', 'POST'])
def cus_feedback():
    msg=""
    act=""
    uname=""
    if 'username' in session:
        uname = session['username']

    print(uname)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname, ))
    data = mycursor.fetchone()

    if request.method=='POST':
        details=request.form['details']

        mycursor.execute("SELECT max(id)+1 FROM cc_feedback")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")

        sql = "INSERT INTO cc_feedback(id,uname,details,rdate) VALUES (%s,%s,%s,%s)"
        val = (maxid,uname,details,rdate)
        
        mycursor.execute(sql, val)
        mydb.commit()

        
        print(mycursor.rowcount, "Registered Success")
        msg="success"

    
    return render_template('cus_feedback.html',data=data,msg=msg)

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

@app.route('/cus_token', methods=['GET', 'POST'])
def cus_token():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(uname,))
    data = mycursor.fetchone()
    

    mycursor.execute("SELECT * FROM cc_token where uname=%s order by id desc",(uname,))
    data2 = mycursor.fetchall()
    
        
    return render_template('cus_token.html',data=data,data2=data2)

@app.route('/cus_reply', methods=['GET', 'POST'])
def cus_reply():

    mycursor = mydb.cursor()
    tid=request.args.get("tid")
    mycursor.execute("SELECT * FROM cc_reply where tid=%s order by id desc",(tid,))
    data = mycursor.fetchall()

    return render_template('cus_reply.html',data=data)


@app.route('/agent_home', methods=['GET', 'POST'])
def agent_home():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent where uname=%s",(uname,))
    data = mycursor.fetchone()
        
    return render_template('agent_home.html',data=data)

@app.route('/agent_token', methods=['GET', 'POST'])
def agent_token():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]

    mycursor.execute("SELECT * FROM cc_token where agent=%s order by id desc",(uname,))
    data2 = mycursor.fetchall()
    
        
    return render_template('agent_token.html',data=data,data2=data2)

@app.route('/agent_img', methods=['GET', 'POST'])
def agent_img():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent where uname=%s",(uname,))
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
            photo="A"+str(aid)+filename
            file.save(os.path.join("static/upload", photo))
            mycursor.execute("update cc_agent set photo=%s where uname=%s",(photo,uname))
            mydb.commit()
            msg="success"
        
    return render_template('agent_img.html',data=data,msg=msg)


@app.route('/agent_pass', methods=['GET', 'POST'])
def agent_pass():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]

    if request.method=='POST':
        oldpass=request.form['oldpass']
        newpass=request.form['newpass']

        mycursor.execute("SELECT count(*) FROM cc_agent where uname=%s && pass=%s",(uname,oldpass))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            mycursor.execute("update cc_agent set pass=%s where uname=%s",(newpass,uname))
            mydb.commit()
            msg="success"
        else:
            msg="wrong"
            

        
    return render_template('agent_pass.html',data=data,msg=msg)

@app.route('/agent_reply', methods=['GET', 'POST'])
def agent_reply():
    msg=""
    uname=""
    tid=request.args.get("tid")
    email=""
    mess=""
    st=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cc_agent where uname=%s",(uname,))
    data = mycursor.fetchone()
    ptype=data[5]

    mycursor.execute("SELECT * FROM cc_token where id=%s",(tid,))
    dd = mycursor.fetchone()
    cus=dd[1]

    mycursor.execute("SELECT * FROM cc_customer where uname=%s",(cus,))
    data1 = mycursor.fetchone()
    email=data1[4]

    if request.method=='POST':
        status=request.form['status']
        reply=request.form['reply']
        mycursor.execute("update cc_token set status=%s where id=%s",(status,tid))
        mydb.commit()

        mycursor.execute("SELECT max(id)+1 FROM cc_reply")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO cc_reply(id,agent,tid,status,reply) VALUES (%s,%s,%s,%s,%s)"
        val = (maxid,uname,tid,status,reply)
        mycursor.execute(sql, val)
        mydb.commit()

        
        mess="Token ID: "+str(tid)+", Problem has solved, reply by "+uname
        #mess="Your problem solved"
        msg="success"
        if status=="2":
            st="1"
            print(email)
            print(mess)
            print("yes")
            subject="Customer Care"
            #url="http://iotcloud.co.in/testmail/testmail1.php?message="+mess+"&email="+email+"&subject="+subject
            #webbrowser.open_new(url)

        
    return render_template('agent_reply.html',data=data,msg=msg,email=email,mess=mess,st=st)


@app.route('/view_token', methods=['GET', 'POST'])
def view_token():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    

    mycursor.execute("SELECT * FROM cc_token order by id desc")
    data2 = mycursor.fetchall()
    print(data2)
        
    return render_template('view_token.html',data2=data2)

@app.route('/view_feedback', methods=['GET', 'POST'])
def view_feedback():
    msg=""
    uname=""
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    

    mycursor.execute("SELECT * FROM cc_feedback order by id desc")
    data2 = mycursor.fetchall()
    
        
    return render_template('view_feedback.html',data2=data2)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
