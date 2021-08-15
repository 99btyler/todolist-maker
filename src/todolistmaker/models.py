from flask_login import UserMixin

from todolistmaker import database, login_manager


class ModelUser(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    picture = database.Column(database.String, nullable=False, default="picture_default.png")
    todolist = ["Test Task"]


@login_manager.user_loader
def load_user(user_id):
    return ModelUser.query.get(user_id)


database.create_all()