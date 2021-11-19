from logging import debug
from flask.templating import render_template
from flask_login.utils import login_user
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from api import *

# some bullshit from the slides
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# so the html files in the templates folder work
bootstrap = Bootstrap(app)

# form classes for the templates in the template folder
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    confpass = PasswordField('confirm password', validators=[InputRequired()])

# some more shit from the slides, returns user by id for some reason idk why
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# redirect main directory to login (should have to login before using app)
@app.route('/')
def index():
    return redirect('/home')

# login directory
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()

    # if method is post then check was was posted, otherwise serve templates/login.html
    if (request.method == 'POST'):
        
        # I think these ifs can be combined but fck it
        # make sure user exists in user table
        if (User.query.filter_by(username = form.username.data).first() is not None):
            # if the user exists then check the password, this way only log in if user exists and password is correct
            if(User.query.filter_by(username = form.username.data).first().password == form.password.data):
                user = User.query.filter_by(username = form.username.data).first()
                login_user(user)
                return redirect('/home')
        else:
            # otherwise tell user to try again
            return '<a href=\'/login\'>wrong username or password, click here to try again</a>'
    
    return render_template('login.html', form = form)


# sing up directory
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if (request.method == 'POST'):
        
        # only add to db if user does not exist
        if (User.query.filter_by(username = form.username.data).first() is not None):
            return '<a href=\'/register\'>username already exists, click here to try again.</a>'
        
        # next make sure passwords match
        if (form.confpass.data != form.password.data):
            return '<a href=\'/register\'>passwords did not match, click here to try again.</a>'
        
        # if username not already taken and passwords match then add to db
        db.session.add(User(username = form.username.data, password = form.password.data))
        db.session.commit()
        return '<a href=\'/login\'>account created, click here to head to login</a>'
    
    # if the request method is not POST then serve the register page.
    return render_template('register.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<a href=\'/login\'>logged out. click here to log back in</p>'

@app.route('/home')
@login_required
def home():
    # check if user_id is a student
    if Student.query.filter_by(user_id = current_user.id).first() is not None:
        
        # if user_id is in student then store the student_id of the user
        student_id = Student.query.filter_by(user_id = current_user.id).first().id
        grades_table = '<tr><th>Course Name</th><th>Instructor</th><th>Time</th><th>Enrolled</th><th>Capacity</th></tr>'
        class_id_list = []

        # build the table of the classes that student is currently in
        for row in Enrollment.query.filter_by(student_id = student_id).all():
            # query elements
            course_name = str(Class.query.filter_by(id = row.class_id).first().course_name)
            instructor =  str(Teacher.query.filter_by(id = Class.query.filter_by(id = row.class_id).first().teacher_id).first().name)
            time = str(Class.query.filter_by(id = row.class_id).first().time)
            enrolled = str(str(Class.query.filter_by(id = row.class_id).first().enrolled))
            capacity = str(str(Class.query.filter_by(id = row.class_id).first().capacity))
            class_id_list.append(row.class_id)
            # print(class_id_list)
            # build table
            grades_table += '<tr> <td>' + course_name + '</td>'
            grades_table += '<td>' + instructor + '</td>'
            grades_table += '<td>' + time + '</td>'
            grades_table += '<td>' + enrolled + '</td>'
            grades_table += '<td>' + capacity + '</td></tr>'
        
        all_classes = '<tr><th>Course Name</th><th>Instructor</th><th>Time</th><th>Enrolled</th><th>Capacity</th><th>Add Course</th></tr>'

        # build the table of offered courses
        for row in Class.query.all():
            course_name = row.course_name
            instructor =  str(Teacher.query.filter_by(id = Class.query.filter_by(id = row.id).first().teacher_id).first().name)
            time = row.time
            enrolled = str(row.enrolled)
            capacity = str(row.capacity)

            # logic for whether or not link to add class should be offered
            if row.id in class_id_list:
                add = '<a href = \'/drop/' + str(row.id) + '\'>drop</a>'
            else:
                if row.enrolled >= row.capacity:
                    add = 'full'
                else:
                    add = '<a href = \'/add/' + str(row.id) + '\'>add</a>'
            
            all_classes += '<tr> <td>' + course_name + '</td>'
            all_classes += '<td>' + instructor + '</td>'
            all_classes += '<td>' + time + '</td>'
            all_classes += '<td>' + enrolled + '</td>'
            all_classes += '<td>' + capacity + '</td>'
            all_classes += '<td>' + add + '</td></tr>'
        return render_template('home.html',name = current_user.username, id = 'student', grades = grades_table, total = all_classes)

    else:
        return render_template('home.html', name = current_user.username, id = 'teacher')

@app.route('/add/<id>')
@login_required
def add(id):
    # could not for the life of me figure out how to have dual column uniqueness with sqla
    # so I do it manually here
    # UNIQUE(CLASS_ID, STUDENT_ID) in enrollment table
    student_id = Student.query.filter_by(user_id = current_user.id).first().id
    class_id_list = []
    for row in Enrollment.query.filter_by(student_id = student_id).all():
        class_id_list.append(row.class_id)
    print(class_id_list)
    if int(id) not in class_id_list:
        db.session.add(Enrollment(class_id = id, student_id = student_id))
        Class.query.filter_by(id = id).first().enrolled += 1
        db.session.commit()
    
    return redirect('/home')

@app.route('/drop/<id>')
@login_required
def drop(id):
    student_id = Student.query.filter_by(user_id = current_user.id).first().id
    enrollment = Enrollment.query.filter_by(class_id = id, student_id = student_id)
    if enrollment.first() is not None:
        enrollment.delete()
        Class.query.filter_by(id = id).first().enrolled -= 1

    db.session.commit()
    return redirect('/home')

if __name__ == '__main__':
    app.run()