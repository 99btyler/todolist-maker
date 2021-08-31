from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import FieldList, FormField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from todolistmaker.models import ModelUser


class FormRegister(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        if ModelUser.query.filter_by(email=email.data).first():
            raise ValidationError("An account with that email already exists.")


class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FormEditAccount(FlaskForm):
    picture = FileField("", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")


class FormTodolistAdd(FlaskForm):
    new_task = StringField()
    submit = SubmitField("+")