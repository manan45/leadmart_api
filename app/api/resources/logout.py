from flask_restful import Resource
from app.api.repositories import UserRepository
from werkzeug.exceptions import BadRequest
from flask_login import login_required, current_user


class Logout(Resource):

    @login_required
    def post(self):
        user_id = current_user.get_id()
        logged_user = UserRepository().logout(user_id)
        if logged_user:
            return {
                "message": "User Logged Out Successfully",
                "is-active": logged_user.is_active,
                "logout_on": str(logged_user.updated),
                "user_id": str(logged_user.user_id)
            }
        raise BadRequest('Error Occurred')
