from enum import unique
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin
from sqlalchemy.orm import joinedload


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
    password = db.Column(db.String, nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, unique=True)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, unique=True)

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True) 
    course_name = db.Column(db.String, unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String, nullable=False)

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True) 
    class_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    grade = db.Column(db.Integer)

