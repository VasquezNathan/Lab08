from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite" 
db = SQLAlchemy(app) 

class User(db.Model): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, auto_increment = True) 
    username = db.Column(db.String, unique=True, nullable=False) 
    email = db.Column(db.String, unique=True, nullable=False)