from flask_restful import Resource
from app.api.repositories import UserRepository
from app.api.adapters.InputAdapters import UserInputAdapter
from app.api.adapters.OutputAdapters import UserOutputAdapter
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_login import current_user, login_required


class UserId(Resource):

    def get(self, user_id):
        if user_id == 'me' and current_user.get_id():
            user_id = current_user.get_id()
        user = UserRepository().get_user(user_id)
        if user:
            return UserOutputAdapter().parse(user)
        raise BadRequest("user details not available")

    @login_required
    def put(self, user_id):
        if user_id == "me":
            user_id = current_user.get_id()
        elif int(user_id) != current_user.get_id():
            raise Unauthorized('You are not allowed yo update this profile')
        parsed_user = UserInputAdapter().parse()
        updated_user = UserRepository().update_user(parsed_user, user_id)
        if updated_user:
            return {
                'message': 'User details updated',
                'user': UserOutputAdapter().parse(updated_user)
            }


