from flask import Flask, request
from app.data_stores import mysql
from flask_login import LoginManager, current_user as _current_user
import app.api
from flask_script import Manager
import json

APP = Flask(__name__)

db = mysql.MYSQL().load(APP)

login_manager = LoginManager()
login_manager.init_app(APP)

current_user = _current_user


def get_current_user():
    return current_user


from app.endpoint_manager import EndpointManager

em = EndpointManager(APP)
em.load()

from app.api.models import UserLogin, User


@login_manager.request_loader
def load_user_from_header(header_val):
    token = request.headers.get('X-Authorization-Token')
    if token:
        user_login = UserLogin.query.filter(UserLogin.token == token, UserLogin.is_active == UserLogin.IS_ACTIVE_TRUE).first()
        if user_login:
            from app.api.repositories import UserRepository
            decoded_token = UserRepository().decode_auth_token(token)
            if decoded_token:
                user = User.query.filter(User.id == decoded_token['user_id']).first()
                if decoded_token['type'] == user.type and decoded_token['email'] == user.email and decoded_token['username'] == user.username and decoded_token['is_active'] == str(user_login.is_active):
                    return user
    return None


@APP.after_request
def parse(response):
    try:
        if response.get_data():
            data = json.loads(response.get_data())
            if not (type(data)) is dict or type(data) is list:
                response.set_data(json.dumps({'message':data}))
            elif 'message' in data:
                response.set_data(json.dumps(data))
            else:
                response.set_data(json.dumps({'data':data}))
                if response.status_code == 200 and (request.method == 'POST'):
                    response.status_code = 201

            return response

    except:
        return response
    return response
