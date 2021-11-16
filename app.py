from flask_admin import Admin 
from flask_admin.contrib import sqla
from api import *

app.secret_key = 'super secret key'

# set optional bootswatch theme
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.sqlite'
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# admin.add_view(ModelView(User, db.session)) 

class UserView(sqla.ModelView): 
    can_delete = False # disable model deletion 
    can_create = False # disable model creation 
    can_edit = False # disable model editing 


admin = Admin(app, name='Gradebook') 
admin.add_view(UserView(User, db.session)) 

db.create_all()
# Add administrative views here
app.run() 