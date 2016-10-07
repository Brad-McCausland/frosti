from flask import Flask, request, render_template, redirect, url_for
import flask
app=flask.Flask(__name__)

import os
import time
import subprocess

def readUserData(type):
    list = []
    file = open(os.path.join(os.path.expanduser('~'),"frostiSrc/alertSrc/user_register/" + type + ".txt"), 'r')
    for line in file:
        if line != '\n':
            list.append(line.split(' ')[0])
    return list

mailinglist = readUserData("email")
print(mailinglist)
phonenumbers = readUserData("phone")

@app.route('/addemail', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.form['newemail']) #subprocess here
        return redirect(url_for('hello'))

@app.route("/")
def hello():
    return render_template('index.html',mailinglist=mailinglist,phonenumbers=phonenumbers)

if __name__ == "__main__":
    app.run(host='localhost',port=5000)
