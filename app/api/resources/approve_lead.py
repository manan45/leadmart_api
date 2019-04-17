from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from app.api.repositories import LeadRepository
from flask_login import current_user, login_required


class ApproveLead(Resource):

    @login_required
    def post(self, lead_id):
        user_type = current_user.get_type()
        lead_status = LeadRepository().approve_lead(lead_id, user_type)
        if lead_status:
            return {
                "message": "Lead Approved"
            }
        raise BadRequest("error occurred")
