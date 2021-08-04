from todolistmaker import database


class ModelUser(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    picture = database.Column(database.String, nullable=False, default="picture_default.png")
    todo_list = database.relationship("ModelTodoList", backref="owner")

class ModelTodoList(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    # ...
    user_id = database.Column(database.Integer, database.ForeignKey("model_user.id"), nullable=False)


database.create_all()