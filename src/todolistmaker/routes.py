from flask import redirect, render_template, url_for

from todolistmaker import app, bcrypt, database
from todolistmaker.forms import FormLogin, FormRegister
from todolistmaker.models import ModelTodoList, ModelUser


@app.route("/register", methods=["GET", "POST"])
def register():
    form_register = FormRegister()
    if form_register.validate_on_submit():
        database.session.add(ModelUser(email=form_register.email.data, password=bcrypt.generate_password_hash(form_register.password.data).decode("utf-8")))
        database.session.commit()
        return redirect(url_for("login"))
    return render_template("pages/register.html", title="Register", form=form_register)

@app.route("/login")
def login():
    return render_template("pages/login.html", title="Login", form=FormLogin())