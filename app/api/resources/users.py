from flask_login import login_required, current_user
from app.api.repositories import AdminRepository
from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from app.api.adapters.OutputAdapters import UserOutputAdapter


class Users(Resource):

    @login_required
    def get(self, type):
        user_type = current_user.get_type()
        users = AdminRepository().view_users_for_admin(user_type, type)
        if users:
            results = []
            for user in users:
                results.append(UserOutputAdapter().parse(user))
            return results
        raise BadRequest("Error in fetching users")





