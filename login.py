from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

login_blueprint = Blueprint('login', __name__)

# Dummy users (Replace with a database in production)
users = {
    "test_user": {"password": "test_pass"},
    "admin": {"password": "password"}
}

# Initialize Flask-Login
login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            login_user(User(username))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form, error="Invalid credentials")
    return render_template('login.html', form=form)

@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))
