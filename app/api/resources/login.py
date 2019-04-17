from flask_restful import Resource
from app.api.adapters.InputAdapters import LoginInputAdapter
from app.api.repositories import UserRepository
from werkzeug.exceptions import BadRequest


class Login(Resource):
    def post(self):
        parsed_login = LoginInputAdapter().parse()
        user = UserRepository().login(parsed_login)
        if user:
            return{
                "message": "User logged in successfully",
                "status": user.is_active,
                "token": user.token
            }
        raise BadRequest('Error Occurred')


