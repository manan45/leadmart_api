from flask_restful import Resource
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from app.api.repositories import AdminRepository


class UserAction(Resource):

    # TODO for admin
    @login_required
    def post(self, user_id, action):
        if user_id == 'me' and current_user.get_id():
            user_id = current_user.get_id()
            action = "BLOCK"
        user_type = current_user.get_type()
        user = AdminRepository().action_on_user(user_id, user_type, action)
        if user:
            return {
                "message": "Action is performed Successfully"
            }
        raise BadRequest("Unable to block")
