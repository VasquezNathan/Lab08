from os import stat
from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask.typing import StatusCode
from flask.wrappers import Request
from werkzeug.wrappers import response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite" 
db = SQLAlchemy(app) 

class Grades(db.Model):
    name = db.Column(db.String, primary_key = True, nullable = False)
    grade = db.Column(db.Integer, nullable = False)

db.create_all()


@app.route('/')
def index():
    return 'index page'

@app.route('/grades/<name>', methods = ['GET'])
def getGrade(name):
    if request.method == 'GET':
        grades = Grades.query.filter_by(name=name).first() 
        if grades == None:
            return response.Response(status=404)
        print(grades.name)
        gradesJson = {}
        gradesJson[grades.name] = grades.grade
        return json.dumps(gradesJson)
        # with open('grades.json', 'r') as gradesFile:
        #     try:
        #         return '{\"' + name + '\":' + str((json.load(gradesFile)[name])) + '}'
        #     except:
        #         return response.Response(status=404)


@app.route('/grades', methods = ['GET', 'POST', 'DELETE'])
def getGrades():
    if request.method == 'GET':
        grades = Grades.query.all()
        gradesJson = {}
        for grade in grades:
            print(grade.name, grade.grade)
            gradesJson[grade.name] = grade.grade
        return json.dumps(gradesJson)

        # with open('grades.json', 'r') as grades:
        #     return grades.read()   
    elif request.method == 'POST':

        crack = json.loads(request.get_data().decode())
        print(list(crack.items())[0][0], list(crack.items())[0][1])

        db.session.add(Grades(name = list(crack.items())[0][0], grade = list(crack.items())[0][1]))
        db.session.commit()
        return response.Response(status=200)
        #     grades = json.load(gradesFile)
        #     grades = json.loads(request.get_data().decode()) | grades
        #     gradesFile.close()

        # with open('grades.json', 'w') as gradesFile:
        #     json.dump(grades, gradesFile, sort_keys=True)
        #     gradesFile.close()
    elif request.method == 'DELETE':
        grades = Grades.query.all()
        gradesJson = {}
        for grade in grades:
            print(grade.name, grade.grade)
            gradesJson[grade.name] = grade.grade
        try:
            gradesJson.pop(request.get_data().decode())
        except:
            return response.Response(status=404)
        Grades.query.filter_by(name=request.get_data().decode()).delete()
        db.session.commit()
        # with open('grades.json', 'r') as gradesFile:
        #     grades = json.load(gradesFile)
        #     print(grades)
        #     try:
        #         grades.pop(request.get_data().decode())
        #         gradesFile.close()
        #     except:
        #         gradesFile.close()
        #         return response.Response(status=404)     
        # with open('grades.json', 'w') as gradesFile:
        #     json.dump(grades, gradesFile, sort_keys=True)
        #     gradesFile.close()
        return response.Response(status=200)

if __name__ == '__main__':
    app.run()
