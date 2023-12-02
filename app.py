from db_interactions import DB_Interface 
from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
@app.route("/login")
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)