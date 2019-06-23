from flask_restful import Resource
from app.api.adapters.InputAdapters import UserInputAdapter
from app.api.adapters.OutputAdapters import UserOutputAdapter
from app.api.repositories import UserRepository


class Register(Resource):

    def post(self):
        parsed_user = UserInputAdapter().parse()
        user = UserRepository().add_user(parsed_user)
        return UserOutputAdapter().parse(user)

