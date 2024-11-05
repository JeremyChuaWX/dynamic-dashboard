from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user
from flask_login.mixins import UserMixin
from flask_login.utils import login_required, logout_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import Email, Length

from environment import Environment

server = Flask(Environment.APP_NAME)
server.config["SECRET_KEY"] = "DYNAMIC DASHBOARD"
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
Bootstrap(server)
db = SQLAlchemy(server)
login = LoginManager()
login.init_app(server)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


migrate = Migrate(server, db)


@login.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=5)])


class RegisterForm(FlaskForm):
    email = StringField("email", validators=[Email()])
    password = PasswordField("password", validators=[Length(min=5)])
    repeat_password = PasswordField("repeated_password", validators=[Length(min=5)])


@server.route("/")
def index():
    return render_template("index.html")


@server.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if check_password_hash(user.password, form.password.data):
            login_user(user)

            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@server.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit() and form.password.data == form.repeat_password.data:
        user = User(
            email=form.email.data, password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@server.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("index"))
