from flask import Flask, flash, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import flask

import os
#import sys
import time
import subprocess


app=flask.Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

class User(UserMixin):
    user_database = {"Admin": ("Admin", "adminpassword"),
               "Admin2": ("Admin2", "megagoodpassword")}
    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)

#this thing needs to find user from db, create instance of and return it.
@login_manager.user_loader
def load_user(id):
    user = User.get(id)
    return User(user[0],user[1])

#path = sys.path[0] #sys.path[0] is directory script was launched from

@app.route('/login',methods=['GET','POST'])
def login():
    #This checks for the username in the 'database'.
    if request.method == 'GET':
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

    flash('Login Failed')
    return flask.redirect(flask.url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#scipt is a string "script.py"
def runScript(script,args):

    path = os.path.join(os.path.expanduser('~'),"frostiSrc/scripts/" + script)
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
    file = open(os.path.join(os.path.expanduser('~'),"frostiSrc/alertSrc/user_register/" + type), 'r')
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

mailinglist = readUserData("email.txt")
phonenumbers = readPhoneData()

@app.route('/addemail', methods=['POST'])
def addemail():
    if request.method == 'POST':
        arg1 = request.form['newemail']
        arg2 = request.form['scope']
        result = runScript("addemail.py",[arg1,arg2])
        global mailinglist
        mailinglist = readUserData("email.txt")

        #return render_template('result.html',scriptResult="taco",hmm=result)
        return redirect(url_for('formresult',scriptResult=result)) #'url_for' wants def name(), not @app.route

@app.route('/deletemail', methods=['POST'])
def deletemail():
    if request.method == 'POST':
        arg1 = request.form['deleteemail']
        result = runScript("deleteemail.py",[arg1])
        global mailinglist
        mailinglist = readUserData("email.txt")

        #return render_template('result.html',scriptResult="taco",hmm=result)
        return redirect(url_for('formresult',scriptResult=result)) #'url_for' wants def name(), not @app.route

@app.route('/addphone', methods=['POST'])
def addphone():
    if request.method == 'POST':
        arg1 = request.form['newphone']
        arg2 = request.form['scope']
        result = runScript("addphone.py",[arg1,arg2])
        global phonenumbers #need this to make main page update properly
        phonenumbers = readUserData("phone.txt")

        return redirect(url_for('formresult',scriptResult=result)) #'url_for' wants def name(), not @app.route

@app.route('/deletephone', methods=['POST'])
def deletephone():
    if request.method == 'POST':
        arg1 = request.form['deletephone']
        result = runScript("deletephone.py",[arg1])
        global phonenumbers
        phonenumbers = readUserData("phone.txt")

        #return render_template('result.html',scriptResult="taco",hmm=result)
        return redirect(url_for('formresult',scriptResult=result)) #'url_for' wants def name(), not @app.route
#just returning a string right now but this shold be set up as a real page with a template
#not used now because of some...problem
#@app.route("/formresult/<scriptResult>")
#def formresult(scriptResult,hmm):
#    return render_template('result.html',
#        scriptResult=scriptResult,hmm=hmm)

@app.route("/formresult")
def formresult():
    return render_template('result.html',scriptResult=request.args.get('scriptResult'))

@app.route("/templogin")
def templogin():
    return render_template('login.html')

@app.route("/")
@login_required
def hello():
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

if __name__ == "__main__":
    app.config["SECRET_KEY"] = '%hwgS\x13\x97\xf4\xee\xf8\xa8< \x11\xd1*\xe8\xecV\x95\xfbeY\xbe'
    app.run(host='0.0.0.0',port=5000)
