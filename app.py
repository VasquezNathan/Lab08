from os import abort
from flask.helpers import url_for
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_login import LoginManager, current_user, login_user, login_required
from flask_login.utils import login_required
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from api import *


# set optional bootswatch theme
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'


# all bullshit from the slides
app.secret_key = 'super secret key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# also bullshit from the slides
@login_manager.user_loader 
def load_user(user_id): 
   return User.get_id(user_id)

# /login directory
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check password against User db
        if User.query.filter_by(username=username).first() is not None and password == User.query.filter_by(username=username).first().password:
            login_user(User.query.filter_by(username=username).first())
            return redirect('admin')
        else:
            return redirect(url_for('login'))
    else:
        return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        '''

# route /admin should need a login before it can be accessed
@app.route('/admin')
@login_required
def hello():
    return response.Response(status=200)

class UserView(sqla.ModelView): 
    can_delete = False # disable model deletion 
    can_create = False # disable model creation 
    can_edit = False # disable model editing 


admin = Admin(app, name='Gradebook') 
admin.add_view(UserView(User, db.session)) 

db.create_all()
# Add administrative views here
app.run() 