from db_interactions import DB_Interface 
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import time
import datetime

file = open('secrets.json')
credentials = json.load(file)
file.close()

DB = DB_Interface()

app = Flask(__name__)

app.secret_key = credentials['secret_key']

@app.route("/")
def home():
    logged_in = valid_session()
    if logged_in:
        return redirect(url_for('dashboard', name=logged_in))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    logged_in = valid_session()
    if logged_in:
        return redirect(url_for('dashboard', name=logged_in))
    else:
        error = None
        if request.method == 'POST':
            user = DB.ret_employee_pwd(request.form['username'], request.form['password'])
            if user == []:
                error = "Invalid credentials. Please try again."
            else:
                session['username'] = request.form['username']
                session['name'] = user[0][1]
                return redirect(url_for('dashboard', name=session['name']))
            
        return render_template('login.html', err_message=error)


@app.route("/dashboard/<name>", methods=["GET", "POST"])
def dashboard(name):
    if valid_session():
        if request.method == 'POST':
            if request.form['review_request'] == "TEST":
                return redirect(url_for('review'))
        else:
            if DB.is_manager(session['username']):
                return render_template('dashboard.html', manager="YES")
            else:
                return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    

@app.route("/review", methods=["GET", "POST"])
def review():
    if valid_session():
        return render_template('review.html')
    else:
        return redirect(url_for('login'))


@app.route("/submit_leave_request", methods=["POST"])
def submit_leave_request():
    if valid_session():
        username = session['username']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        reason = request.form.get('reason', '')

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        try:
            DB.add_leave_request(username, start_date, end_date, reason)
            flash('Leave request submitted successfully', 'success')
        except Exception as e:
            print("Error submitting leave request:", e)
            flash('Error. Please try again', 'error')
        
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    
@app.route("/submit_WFH_request", methods=['POST'])
def submit_WFH_request():
    if valid_session():
        username = session['username']
        date = request.form['date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        try:
            DB.add_wfh_day(username, date)
            flash('WFH request submitted successfully', 'success')
        except Exception as e:
            print("Error submitting leave request:", e)
            flash('Error. Please try again', 'error')
        
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))



        







@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('review'))


def valid_session():
    """
    Checks if a user session exists

    Returns:
    bool: False if session doesn't exist
    str: Name of logged in user
    """
    try:
        return session['name']
    except KeyError:
        return False


if __name__ == "__main__":
    app.run(debug=True)