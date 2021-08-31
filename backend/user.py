from flask import abort, make_response
from sqlalchemy import exc
from models import User, UserSchema
from config import db

def create(user):
    """
    /api/user
    """
    username = user.get("username")
    email = user.get("email")
    password = user.get("password")
    try:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    
    except exc.IntegrityError:
        abort(
                400, f'Video with username "{username}" or the email "{email}" already exsists'
            ) 
    
    return make_response(f'"{username}" sucessfully created', 201)


def read_all():
    """
    /api/users
    """
    users = User.query.all()

    user_schema = UserSchema(many=True)
    return user_schema.dump(users)


def read_one(username):
    """
    /api/users/{username}
    """
    user = User.query.filter_by(username=username).first()
    user_schema = UserSchema(many=False)
    if user:
        return user_schema.dump(user)
    else:
        abort(
            404, f'User with username "{username}" not found'
        )


def update(username, user):
    user_to_change = User.query.filter_by(username=username).first()
    user_schema = UserSchema(many=False)
    if user:
        user_to_change.username = user.get("username", None)
        user_to_change.email = user.get("email", None)
        user_to_change.password = user.get("password", None)

        db.session.commit()

        return user_schema.dump(user_to_change)
    else:
        abort(
            404, f'User with username "{username}" not found'
        )

def delete(username):
    user = User.query.filter_by(username=username).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return make_response(f'{username} successfully deleted')
    else:
        abort(
            404, f'User with username {username} not found'
        )