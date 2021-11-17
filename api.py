from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/nathanvasquez/Developer/CSE_106/Lab08/example.sqlite'
app.config['SECRET_KEY'] = 'fucking shit'
db = SQLAlchemy(app) 


# create the user table with schema user(id, username, password)
class User(UserMixin, db.Model): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String, unique=True, nullable=False) 
    password = db.Column(db.String, unique=True, nullable=False)

db.create_all()