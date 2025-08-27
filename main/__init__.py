from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
import os

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME = 'franchise_brand.db'


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def __init__(self, *args, **kwargs):
        super(MyAdminIndexView, self).__init__(*args, **kwargs)
        self.static_folder = 'static'


class MyUserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    # Правильная форма для role
    form_overrides = {
        'role': SelectField
    }
    form_args = {
        'role': dict(
            choices=[('user', 'User'), ('admin', 'Admin')],
            coerce=str
        )
    }
    form_create_rules = ['email', 'password', 'role']
    form_edit_rules = ['role']


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'franchise_brand'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
    db.init_app(app)

    # Flask-Admin
    admin = Admin(app, name='FRANCHISE BRAND ADMIN', index_view=MyAdminIndexView())

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)

    from main.models import User, Product, Category, Gallery, Order, NewDrop
    admin.add_view(MyModelView(Order, db.session))
    admin.add_view(MyUserView(User, db.session))
    admin.add_view(MyModelView(Product, db.session))
    admin.add_view(MyModelView(Category, db.session))
    admin.add_view(MyModelView(Gallery, db.session))
    admin.add_view(MyModelView(NewDrop, db.session))

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from main.views import views
    from main.auth import auth
    from main.upload import adm
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(adm, url_prefix='/')

    return app