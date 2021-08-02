import os

from flask import Flask, render_template, url_for

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32).hex()

# POST
class FormRegister(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/post")
def post():
    return render_template("pages/post.html", title="Register", form=FormRegister())


if __name__ == "__main__":
    app.run(debug=True)