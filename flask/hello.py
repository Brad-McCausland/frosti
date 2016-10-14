from flask import Flask, request, render_template, redirect, url_for
import flask
app=flask.Flask(__name__)

import os
#import sys
import time
import subprocess

#path = sys.path[0] #sys.path[0] is directory script was launched from

#scipt is a string "script.py"
def runScript(script,arg1,arg2):
    path = os.path.join(os.path.expanduser('~'),"frostiSrc/scripts/" + script)
    process = subprocess.Popen(["python3",path,arg1,arg2],stdout=subprocess.PIPE)
    result = process.stdout.read()
    return result

def readUserData(type):
    list = []
    file = open(os.path.join(os.path.expanduser('~'),"frostiSrc/alertSrc/user_register/" + type), 'r')
    for line in file:
        if line != '\n':
            list.append(line.split(' ')[0])
    return list

mailinglist = readUserData("email.txt")
phonenumbers = readUserData("phone.txt")

@app.route('/addemail', methods=['POST'])
def addemail():
    if request.method == 'POST':
        arg1 = request.form['newemail']
        arg2 = request.form['scope']
        result = runScript("addemail.py",arg1,arg2)
        global mailinglist
        mailinglist = readUserData("email.txt") #ehhhhhhhhhhhhh

        return result
        #make real page
        return redirect(url_for('formresult')) #'url_for' wants def name(), not @app.route

@app.route('/addphone', methods=['POST'])
def addphone():
    if request.method == 'POST':
        arg1 = request.form['newphone']
        arg2 = request.form['scope']
        result = runScript("addphone.py",arg1,arg2)

        return result

        return redirect(url_for('formresult')) #'url_for' wants def name(), not @app.route

#just returning a string right now but this shold be set up as a real page with a template
@app.route("/formresult")
def formresult():
    return replaceThis

@app.route("/")
def hello():
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

if __name__ == "__main__":
    app.run(host='localhost',port=5000)
