from flask import Flask, request, render_template, redirect, url_for
import flask
app=flask.Flask(__name__)

import os
#import sys
import time
import subprocess

#path = sys.path[0] #sys.path[0] is directory script was launched from

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

@app.route("/")
def hello():
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

if __name__ == "__main__":
    app.run(host=140.160.44.116,port=5000)
