from flask_restful import Resource
from app.api.adapters.InputAdapters import LeadInputAdapter
from app.api.repositories import LeadRepository
from flask_login import current_user, login_required
from app.api.adapters.OutputAdapters import LeadOutputAdapter
from werkzeug.exceptions import BadRequest


class Lead(Resource):

    @login_required
    def post(self):
        user_id = current_user.get_id()
        user_type = current_user.get_type()
        parsed_lead = LeadInputAdapter().parse()
        lead = LeadRepository().add_lead(parsed_lead, user_id, user_type)
        if lead:
            return LeadOutputAdapter().parse(lead)
        raise BadRequest("Error in adding lead")

    @login_required
    def get(self):
        user_id = current_user.get_id()
        user_type = current_user.get_type()
        lead_details = LeadRepository().get_lead_by_user_id(user_id, user_type)
        details = []
        for lead_detail in lead_details:
            details.append(LeadOutputAdapter().parse(lead_detail))
        return details
