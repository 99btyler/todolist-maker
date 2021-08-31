import os

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from todolistmaker import app, bcrypt, database
from todolistmaker.forms import FormEditAccount, FormTodolistAdd, FormLogin, FormRegister
from todolistmaker.models import ModelTodolistItem, ModelUser


@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        user = ModelUser.query.filter_by(email=current_user.email).first()
        form_todolist_add = FormTodolistAdd()
        if form_todolist_add.validate_on_submit():
            new_todolist_item = ModelTodolistItem(task=form_todolist_add.new_task.data, user_id=user.id)
            database.session.add(new_todolist_item)
            database.session.commit()
            return redirect(url_for("home"))
        return render_template("pages/home.html", form=form_todolist_add, todolist_items=ModelTodolistItem.query.filter_by(user_id=user.id))
    else:
        return render_template("pages/home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form_register = FormRegister()
    if form_register.validate_on_submit():
        # ...
        new_user = ModelUser(email=form_register.email.data, password=bcrypt.generate_password_hash(form_register.password.data).decode("utf-8"))
        database.session.add(new_user)
        database.session.commit()
        # ...
        new_todolist_item = ModelTodolistItem(task="Task 1", user_id=new_user.id)
        database.session.add(new_todolist_item)
        database.session.commit()
        # ...
        return redirect(url_for("login"))
    else:
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
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
    return render_template("pages/login.html", title="Login", form=form_login)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form_edit_account = FormEditAccount()
    if form_edit_account.validate_on_submit() and form_edit_account.picture.data:
        # ...
        _, picture_extension = os.path.splitext(form_edit_account.picture.data.filename)
        picture_name = f"{os.urandom(8).hex()}{picture_extension}"
        # ...
        picture = Image.open(form_edit_account.picture.data)
        picture.thumbnail((125, 125))
        picture.save(os.path.join(app.root_path, "static/pictures", picture_name))
        # ...
        current_user.picture = picture_name
        database.session.commit()
        return redirect(url_for("account"))
    else:
        return render_template("pages/account.html", title="Account", form=form_edit_account, picture=url_for("static", filename=f"pictures/{current_user.picture}"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))