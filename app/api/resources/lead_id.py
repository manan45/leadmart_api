from flask_restful import Resource
from app.api.adapters.InputAdapters import LeadInputAdapter
from app.api.adapters.OutputAdapters import LeadOutputAdapter
from werkzeug.exceptions import BadRequest
from flask_login import login_required, current_user
from app.api.repositories import LeadRepository


class LeadId(Resource):

    @login_required
    def get(self, lead_id):
        user_type = current_user.get_type()
        lead = LeadRepository().get_lead_by_lead_id(lead_id, user_type)
        if lead:
            return LeadOutputAdapter().parse(lead)
        raise BadRequest('Lead Not Available')

    @login_required
    def put(self, lead_id):
        user_id = current_user.get_id()
        user_type = current_user.get_type()
        parsed_lead = LeadInputAdapter().parse()
        lead = LeadRepository().update_lead(parsed_lead, lead_id, user_id, user_type)
        if lead:
            return LeadOutputAdapter().parse(lead)
        raise BadRequest('Error in updating lead')

    @login_required
    def delete(self, lead_id):
        user_id = current_user.get_id()
        user_type = current_user.get_type()
        deleted_lead = LeadRepository().delete_lead(user_id, user_type, lead_id)
        if deleted_lead:
            return {
                "message": "Lead Deleted Successfully"
            }
        raise BadRequest("Error Occurred")
