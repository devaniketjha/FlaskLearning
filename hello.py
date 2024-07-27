from flask import Flask, render_template, abort, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Load the .env file
load_dotenv()
# =======================================================================#
# INFO: Global Settings and Standard Setup for Flask Application
# =======================================================================#

# Crete a Flask Instance
app = Flask(__name__)

# Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# OLD SQL Lite database settings: Use absolute path to avoid relative path issues

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'our_users.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True  # Enable SQLAlchemy echo for debugging


# New MySQL db
mySQLkey = os.getenv('SQL_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{mySQLkey}@localhost/our_users'



# Access the environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the Database
db = SQLAlchemy(app)

# =======================================================================#
# INFO: All the routes will be here.
# =======================================================================#

# Create a route decorator
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/name", methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",
                           name = name,
                           form = form)
    
    
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

@app.route("/user/add", methods = ["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Users(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form,
                           name = name,
                           our_users = our_users)


@app.route('/error')
def error():
    abort(500)  # This will raise a 500 Internal Server Error


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# =======================================================================#
# INFO: The classes will be here down below:
# =======================================================================#
# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    date_added = db.Column(db.DateTime, default = datetime.now)
    
    # Create a String
    def __repr__(self):
        return '<Name %r' %self.name

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a User Form Class
class UserForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    email = StringField("What's Your Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

































if __name__ == '__main__':
    app.run(debug=True)