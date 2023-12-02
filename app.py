from db_interactions import DB_Interface 
from flask import Flask, render_template, request, redirect, url_for, session
import json
import datetime

file = open('secrets.json')
credentials = json.load(file)
file.close()

DB = DB_Interface()

app = Flask(__name__)

app.secret_key = credentials['secret_key']

@app.route("/")
def home():
    try:
        return redirect(url_for('dashboard', username=session['username']))
    except KeyError:
        return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        user = DB.ret_employee_pwd(request.form['username'], request.form['password'])
        if user == []:
            error = "Invalid credentials. Please try again."
        else:
            session['username'] = request.form['username']
            return redirect(url_for('dashboard', username=request.form['username']))
    
    return render_template('login.html', err_message=error)


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)