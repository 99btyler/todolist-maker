from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from todolistmaker import app, bcrypt, database
from todolistmaker.forms import FormLogin, FormRegister
from todolistmaker.models import ModelTodoList, ModelUser


@app.route("/")
def home():
    return render_template("pages/home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form_register = FormRegister()
    if form_register.validate_on_submit():
        database.session.add(ModelUser(email=form_register.email.data, password=bcrypt.generate_password_hash(form_register.password.data).decode("utf-8")))
        database.session.commit()
        return redirect(url_for("login"))
    return render_template("pages/register.html", title="Register", form=form_register)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form_login = FormLogin()
    if form_login.validate_on_submit():
        potential_user = ModelUser.query.filter_by(email=form_login.email.data).first()
        if potential_user and bcrypt.check_password_hash(potential_user.password, form_login.password.data):
            login_user(potential_user)
            potential_next_page = request.args.get("next")
            return redirect(potential_next_page) if potential_next_page else redirect(url_for("home"))
    return render_template("pages/login.html", title="Login", form=form_login)

@app.route("/account")
@login_required
def account():
    return render_template("pages/account.html", title="Account", picture=url_for("static", filename=f"pictures/{current_user.picture}"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))