import os

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from todolistmaker import app, bcrypt, database
from todolistmaker.forms import FormEditAccount, FormEditTodolist, FormLogin, FormRegister
from todolistmaker.models import ModelUser


# GET
@app.route("/")
def home():
    form_edit_todolist = FormEditTodolist(tasks=current_user.tasks) if current_user.is_authenticated else "null"
    return render_template("pages/home.html", form=form_edit_todolist)

@app.route("/register", methods=["GET", "POST"])
def register():
    # ...
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # ...
    form_register = FormRegister()
    if form_register.validate_on_submit():
        database.session.add(ModelUser(email=form_register.email.data, password=bcrypt.generate_password_hash(form_register.password.data).decode("utf-8")))
        database.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("pages/register.html", title="Register", form=form_register)

@app.route("/login", methods=["GET", "POST"])
def login():
    # ...
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # ...
    form_login = FormLogin()
    if form_login.validate_on_submit():
        potential_user = ModelUser.query.filter_by(email=form_login.email.data).first()
        if potential_user and bcrypt.check_password_hash(potential_user.password, form_login.password.data):
            login_user(potential_user)
            potential_next_page = request.args.get("next")
            return redirect(potential_next_page) if potential_next_page else redirect(url_for("home"))
        else:
            return render_template("pages/login.html", title="Login", form=form_login) 
    else:
        return render_template("pages/login.html", title="Login", form=form_login)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # ...
    form_edit_account = FormEditAccount()
    if form_edit_account.validate_on_submit() and form_edit_account.picture.data:
        # save picture
        _, picture_extension = os.path.splitext(form_edit_account.picture.data.filename)
        picture_name = f"{os.urandom(8).hex()}{picture_extension}"
        picture = Image.open(form_edit_account.picture.data)
        picture.thumbnail((125, 125))
        picture.save(os.path.join(app.root_path, "static/pictures", picture_name))
        # update
        current_user.picture = picture_name
        database.session.commit()
        return redirect(url_for("account"))
    else:
        return render_template("pages/account.html", title="Account", form=form_edit_account, picture=url_for("static", filename=f"pictures/{current_user.picture}"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))