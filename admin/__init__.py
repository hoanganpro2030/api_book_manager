from flask import render_template
from flask_admin import Admin
from flask_login import LoginManager
from flask_security import Security

from .models import db, User, Role, user_datastore, Authors, Books
from .views import UserView, RoleView, BookView, AuthorView, WmsAdminIndexView


# Initialize admin
def init_app(app):
    # Initialize the Flask-Security
    security = Security(app, user_datastore)

    # Flask views
    @app.route('/')
    def index():
        return render_template('index.html')

    # Initialize flask-login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    # Create admin
    admin = Admin(app, 'Admin', index_view=WmsAdminIndexView(), base_template='wms_master.html')

    # Add view
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoleView(Role, db.session))
