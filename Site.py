from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import hashlib
import datetime
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY']='C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
Bootstrap(app)

class registerForm(FlaskForm):
    name = StringField('Accout Name', validators=[DataRequired()])
    name1 = StringField('Password?', validators=[DataRequired()])
    submit = SubmitField('Register')

class loginForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired()])
    name1 = StringField('Password?', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/index', methods=['GET', 'POST'])
def main():
    try:
        if validateLoggedin() == True:
            return render_template('index.html')
        else:
            return '<h1> Login Required </h1>'
    except:
        return '<h1> Login Required </h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    con = sqlite3.connect('test.db', check_same_thread=False)
    cur = con.cursor()
    form1 = loginForm()
    message=""
    if form1.validate_on_submit():
        name = form1.name.data
        password = form1.name1.data
        if checkValidity(name,password) == True:
            session['uid'] = uuid.uuid4()
            asd = str(session['uid'])
            cur.execute("UPDATE Users SET sessionID=? WHERE accID=?", (asd, name))
            con.commit()    
            con.close()
            message = "Login Succesful"
            return render_template('index.html')
        else:
            message = "Login Unsuccesful"
            return render_template('login.html', form=form1, message=message)
    else:
        return render_template('login.html', form=form1, message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        password = form.name1.data
        saveCredentials(name, password)
        return 'Registration Complete'
    else:
        return render_template('register.html', form=form, message=message)

def saveCredentials(name, password):
        con = sqlite3.connect('test.db', check_same_thread=False)
        cur = con.cursor()
        salt = os.urandom(32)
        key = hashlib.md5(password.encode())
        storage = key.digest()
        try:
            cur.execute("create table Users (date, accID, passHash, sessionID)")
        except:
            pass
        time = datetime.datetime.now()   
        cur.execute("insert into Users values (?, ?, ?, ?)", (time, name, storage, 'sessionID'))
        con.commit()
        con.close()

def checkValidity(name,password):
    con = sqlite3.connect('test.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("select * from Users where accID=:accID", {"accID": name})
    list1 = cur.fetchall()
    try:
        hash2 = list1[0][2]
    except:
        return False
    hash1 = hashlib.md5(password.encode())
    key1 = hash1.digest()
    con.close()
    if key1 == hash2:
        return True
    else:
        return False

def validateLoggedin():    
    con = sqlite3.connect('test.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("select * from Users")
    allUsers = cur.fetchall()
    con.close()
    print(allUsers[0][3])
    print(session['uid'])
    if allUsers[0][3] == str(session['uid']):
        return True
    else:
        return False
    

    
if __name__ == '__main__':
   app.run(debug=True, port = 8081)