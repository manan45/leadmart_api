from flask_restful import Resource
from app.api.adapters.InputAdapters import LoginInputAdapter
from app.api.repositories import UserRepository
from werkzeug.exceptions import BadRequest
from app.api.models import User


class Login(Resource):
    def post(self):
        parsed_login = LoginInputAdapter().parse()
        user = UserRepository().login(parsed_login)
        if user:
            if user.user_type == int(User.TYPE['admin']):
                user_type = "admin"
            elif user.user_type == int(User.TYPE['super_admin']):
                user_type = "super_admin"
            else:
                user_type = "user"
            return{
                "message": "User logged in successfully",
                "status": user.is_active,
                "token": user.token,
                "user_type": user_type
            }
        raise BadRequest('Error Occurred')


