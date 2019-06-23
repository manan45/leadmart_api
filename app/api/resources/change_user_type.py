from flask_restful import Resource
from flask_login import login_required, current_user
from app.api.repositories import AdminRepository
from werkzeug.exceptions import BadRequest


# functionality only for super admin
class RemoveAdmin(Resource):

    @login_required
    def post(self, demote):  # demote is the user_id of admin that has to be removed
        user_type = current_user.get_type()
        demoted_user = AdminRepository().demote_the_admin(user_type, demote)
        if demoted_user:
            return {
                "message": "Admin is Removed from the list"
            }
        raise BadRequest("Error in removing admin")


class MakeAdmin(Resource):

    @login_required
    def post(self, promote):  # promote is the user_id of admin that has to be removed
        user_type = current_user.get_type()
        promoted_user = AdminRepository().promote_the_user(user_type, promote)
        if promoted_user:
            return {
                "message": "User is promoted to admin"
            }
        raise BadRequest("Error in removing admin")
