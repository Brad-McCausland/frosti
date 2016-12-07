from flask import Flask, flash, request, render_template, redirect, url_for, Response, send_from_directory
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

import flask
import random
import os
import json
import sys
import time
import subprocess
import datetime

filedir = os.path.dirname(os.path.abspath(__file__))
rootdir = filedir[::-1].split('/',1)[1][::-1]

sys.path.append(os.path.abspath(rootdir + "/loggerSrc"))
sys.path.append(os.path.abspath(rootdir + "/alertSrc"))

import logger
from alert import authenticate

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

    path = (rootdir + "/scripts/" + script)
    command = ["python3",path]
    for each in args:
        command.append(each)
    process = subprocess.Popen(command,stdout=subprocess.PIPE)
    result = process.stdout.read()
    return result

#Generic read for user_register info. User for reading in phone and emails form file
def readUserData(type):
    list = []
    file = open(rootdir + "/alertSrc/user_register/" + type, 'r')
    for line in file:
        if line != '\n':
            list.append(line.split(' ')[0])
    return list

def fetchphones():
        errorFile = open(rootdir + "/logs/portalTestlogs.txt",'a')
        sid, token, client = authenticate(errorFile)
        #Fetch list of registered phones
        try:
                caller_ids = client.caller_ids.list()
        except TwilioRestException as e:
                return -1

        for each in caller_ids:
                print(each.phone_number)
        return 0
#processes phone numbers so human can read properly
def readPhoneData():
    list = []
    for number in readUserData("phone.txt"):
        list.append(number[2:5] + '-' + number[5:8] + '-' + number[8:])
    return list

@app.route('/fetchphones')
def sstream():
    def foo():
        errorFile = open("/mnt/e/Dropbox/Docs/frostiGit/frosti/logs/portalTestlogs.txt",'a')
        sid, token, client = authenticate(errorFile)
        #Fetch list of registered phones
        caller_ids = client.caller_ids.list()
        for number in caller_ids:
            yield(str(number.phone_number[2:5] + '-' + number.phone_number[5:8] + '-' + number.phone_number[8:]).rstrip()+',')

    return app.response_class(foo(), mimetype='text/plain')

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
def graphredirect():
    return redirect("/graphs/today")

@app.route("/graphs/<date>",methods=['GET','POST'])
@login_required
def graphs(date):

    if request.method == 'POST':
        if date == "today":
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        return send_from_directory(rootdir + "/logs",date+'.csv',as_attachment=True,attachment_filename=date+'.csv')

    if date != "today":
        if logger.logExist(date):
            dates,f1,f2,f3 = logger.getLogDate(date)
        else:
            return redirect("/graphs/today")
    else:
        dates,f1,f2,f3 = logger.getLogDate("today")

    return render_template('graphs.html',date=date,dates=dates,f1=f1,f2=f2,f3=f3)



@app.route("/frosti")
@login_required
def frosti():
    mailinglist = readUserData("email.txt")
    phonenumbers = readPhoneData()
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

@app.route("/")
def hello():
    return flask.redirect(flask.url_for('login'))
#
if __name__ == "__main__":
    app.config["SECRET_KEY"] = '%hwgS\x13\x97\xf4\xee\xf8\xa8< \x11\xd1*\xe8\xecV\x95\xfbeY\xbe'
    app.run(host='0.0.0.0',port=5000,threaded=True)
