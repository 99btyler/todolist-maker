from flask import render_template

from todolistmaker import app
from todolistmaker.forms import FormRegister
from todolistmaker.models import ModelTodoList, ModelUser


@app.route("/post")
def post():
    return render_template("pages/post.html", title="Register", form=FormRegister())