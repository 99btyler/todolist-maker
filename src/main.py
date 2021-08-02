import os

from flask import Flask, render_template, url_for

from flask_wtf import FlaskForm

from flask_sqlalchemy import SQLAlchemy

from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

database = SQLAlchemy(app)

class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    picture = database.Column(database.String, nullable=False, default="picture_default.png")
    todo_list = database.relationship("TodoList", backref="user")

class TodoList(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    # ...
    user_id = database.Column(database.Integer, database.ForeignKey("user.id"), nullable=False)


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