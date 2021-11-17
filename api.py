from flask import Flask, request, Response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite" 
db = SQLAlchemy(app) 


# create the user table with schema user(id, username, password)
class User(db.Model): 
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, auto_increment = True) 
    username = db.Column(db.String, unique=True, nullable=False) 
    password = db.Column(db.String, unique=True, nullable=False)


    # flask login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # something to do with admin interface
    def check_password(self, password): 
        return self.password == password
