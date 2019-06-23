from flask_restful import Resource
from app.api.repositories import AdminRepository
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest
from app.api.adapters.OutputAdapters import LeadOutputAdapter


class AdminLeads(Resource):

    @login_required
    def get(self, action):
        user_type = current_user.get_type()
        user_id = current_user.get_id()
        leads = AdminRepository().get_leads_for_admin(user_id, user_type, action)
        if leads:
            results = []
            for lead in leads:
                results.append(LeadOutputAdapter().parse(lead))
            return results
        raise BadRequest("Error Occurred")
