from db_interactions import DB_Interface 
from flask import Flask, render_template, request, redirect, url_for, session, flash
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
                session['name'] = user[0]['empl_name']
                return redirect(url_for('dashboard', name=session['name']))
            
        return render_template('login.html', err_message=error)


@app.route("/dashboard/<name>", methods=["GET", "POST"])
def dashboard(name):
    if valid_session():
        if request.method == 'POST':

            if 'cancel_wfh' in request.form:
                date = datetime.datetime.strptime(request.form['cancel_wfh'], '%Y-%m-%d')
                if date < datetime.datetime.today():
                    flash('Error. Cannot Cancel Past or Current Work From Home Day', 'wfh_error')
                else:
                    DB.del_wfh_day(session['username'], datetime.datetime.strptime(request.form['cancel_wfh'], '%Y-%m-%d'))

            elif 'cancel_leave' in request.form:
                leave_req = DB.ret_leave_request_id(int(request.form['cancel_leave']))
                if leave_req != []:
                    leave_req = leave_req[0]
                    if datetime.date.today() > leave_req['req_end_date']:
                        flash('Error. Cannot Cancel Past Leave Request', 'leave_request_error')
                    elif datetime.date.today() >= leave_req['req_start_date'] and datetime.date.today() <= leave_req['req_end_date']:
                        flash('Error. Cannot Cancel Ongoing Leave Request', 'leave_request_error')
                    else:
                        DB.del_leave_request(leave_req['req_id'])

        time_off_requests = DB.ret_leave_request_week(session['username'], datetime.datetime.today())
        wfh_days = DB.ret_wfh_day_week(session['username'], datetime.datetime.today())

        if DB.is_manager(session['username']):
            return render_template('dashboard.html', requests=time_off_requests, days=wfh_days, manager="YES")
        else:
            return render_template('dashboard.html', requests=time_off_requests, days=wfh_days)
    else:
        return redirect(url_for('login'))
    

@app.route("/review", methods=["GET", "POST"])
def review():
    if valid_session():
        if request.method == 'POST':
            if 'approve' in request.form:
                DB.update_leave_request(request.form['approve'], "APPROVED")
            else:
                DB.update_leave_request(request.form['decline'], "DECLINED")

        pending_requests = DB.ret_status_leave_requests(session['username'], "PENDING")
        if valid_session():
            return render_template('review.html', requests=pending_requests)
        else:
            return redirect(url_for('login'))
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

        if end_date < start_date:
            flash('Error. End Date Cannot Be Before Start Date', 'leave_request_error')
        elif start_date < datetime.datetime.today() - datetime.timedelta(1) or end_date < datetime.datetime.today() - datetime.timedelta(1):
            flash('Error. Selected Dates Cannot Be Past Dates', 'leave_request_error')
        elif DB.request_overlapping(username, start_date, end_date):
            flash('Error. Selected Dates Overlap With Existing Leave Request', 'leave_request_error')
        else:
            if DB.add_leave_request(username, start_date, end_date, reason) == False:
                flash('Error. Please try again', 'leave_request_error')
        
        return redirect(url_for('dashboard', name=session['name']))
    else:
        return redirect(url_for('login'))
    

@app.route("/submit_WFH_request", methods=['POST'])
def submit_WFH_request():
    if valid_session():
        username = session['username']
        date = request.form['date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        if date <= (datetime.datetime.today() - datetime.timedelta(1)):
            flash('Error. Selected Date Cannot Be a Past Date', 'wfh_error')
        elif date.weekday() == 5 or date.weekday() == 6:
            flash('Error. Cannot Schedule Work From Home Days on Weekends', 'wfh_error')
        elif DB.wfh_day_overlapping(username, date):
            flash('Error. Date is Already Booked', 'wfh_error')
        elif not DB.valid_wfh_day(username, date, 3):
            flash('Error. Cannot Schedule More Than 3 WFH Days Per Week', 'wfh_error')
        else:
            if DB.add_wfh_day(username, date) == False:
                flash('Error. Please try again', 'wfh_error')
            
        return redirect(url_for('dashboard', name=session['name']))
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('login'))


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
    app.run()