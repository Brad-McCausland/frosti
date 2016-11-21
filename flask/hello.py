from flask import Flask, flash, request, render_template, redirect, url_for, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

import flask
import random
import os
import json
import sys
import time
import subprocess

sys.path.insert(0,"/home/pi/frosti/loggerSrc")
import logger
app=flask.Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

class User(UserMixin):

    def load_database():
        f = open("users.txt")
        user_database = json.load(f)
        return user_database

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.load_database().get(id)

#this thing needs to find user from db, create instance of and return it.
@login_manager.user_loader
def load_user(id):
    user = User.get(id)
    return User(user[0],user[1])

@app.route('/login',methods=['GET','POST'])
def login():
    #This checks for the username in the 'database'.
    if request.method == 'GET':
        if current_user.is_authenticated:
            return flask.redirect(flask.url_for('frosti'))
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    rememberme = False
    if 'rememberme' in request.form:
        rememberme = True

    dbResult = User.get(username)
    if dbResult is not None:
    #Yep, so we send login_user a user, AND the user_loader thing also makes one.
        user = User(dbResult[0],dbResult[1])
        if password == user.password:
            login_user(user, remember = rememberme)
            flash('Login Successful')
            next = flask.request.args.get('next')
            return flask.redirect(flask.url_for('hello'))

    error = 'Incorrect username or password'
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#scipt is a string "script.py"
def runScript(script,args):

    path = os.path.join(os.path.expanduser('~'),"frosti/scripts/" + script)
    command = ["python3",path]
    for each in args:
        command.append(each)
    process = subprocess.Popen(command,stdout=subprocess.PIPE)
    result = process.stdout.read()
    return result

#Generic read for user_register info. Might should move to own file
#with methods instead of strings since phone needs processed anyway and the only
#other one is email
def readUserData(type):
    list = []
    file = open(os.path.join(os.path.expanduser('~'),"frosti/alertSrc/user_register/" + type), 'r')
    for line in file:
        if line != '\n':
            list.append(line.split(' ')[0])
    return list

#processes phone numbers so human can read properly
def readPhoneData():
    list = []
    for number in readUserData("phone.txt"):
        list.append(number[2:5] + '-' + number[5:8] + '-' + number[8:])
    return list

@app.route('/addemail', methods=['POST'])
def addemail():
    if request.method == 'POST':
        arg1 = request.form['newemail']
        arg2 = request.form['scope']
        result = runScript("addemail.py",[arg1,arg2])
        return redirect(url_for('formresult',scriptResult=result))

@app.route('/deletemail', methods=['POST'])
def deletemail():
    if request.method == 'POST':
        arg1 = request.form['deleteemail']
        result = runScript("deleteemail.py",[arg1])
        return redirect(url_for('formresult',scriptResult=result))

@app.route('/addphone', methods=['POST'])
def addphone():
    if request.method == 'POST':
        arg1 = request.form['newphone']
        arg2 = request.form['scope']
        result = runScript("addphone.py",[arg1,arg2])
        return redirect(url_for('formresult',scriptResult=result))

@app.route('/deletephone', methods=['POST'])
def deletephone():
    if request.method == 'POST':
        arg1 = request.form['deletephone']
        result = runScript("deletephone.py",[arg1])
        return redirect(url_for('formresult',scriptResult=result)) #'url_for' wants def name(), not @app.route

@app.route("/formresult")
def formresult():
    return render_template('result.html',scriptResult=request.args.get('scriptResult'))

#replace this with a call to indefinite
#firefox works fine with a real "stream", but chrome wont update until the script is done.?!
@app.route('/graph_stream')
def gstream():
    def foo():
        x = 0
        while(x<1):
            time.sleep(1)
            yield(str(-random.randint(78,81)).rstrip()+',')
            x+=1
    return app.response_class(foo(), mimetype='text/plain')

@app.route("/graphs")
@login_required
def graphs():
    dates = logger.getLogs(10,0,0)
    f1 = logger.getLogs(10,1,0)
    f2 = logger.getLogs(10,2,0)
    f3 = logger.getLogs(10,3,0)
    return render_template('graphs.html',f1=f1,f2=f2,f3=f3,dates=dates)

@app.route("/frosti")
@login_required
def frosti():
    mailinglist = readUserData("email.txt")
    phonenumbers = readPhoneData()
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

@app.route("/")
def hello():
    return flask.redirect(flask.url_for('login'))

if __name__ == "__main__":
    app.config["SECRET_KEY"] = '%hwgS\x13\x97\xf4\xee\xf8\xa8< \x11\xd1*\xe8\xecV\x95\xfbeY\xbe'
    app.run(host='0.0.0.0',port=5000,threaded=True)
