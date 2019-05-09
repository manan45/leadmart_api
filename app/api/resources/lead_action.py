from app.api.repositories import LeadRepository
from flask_restful import Resource
from app.api.adapters.OutputAdapters import LeadOutputAdapter
from flask_login import login_required, current_user
from werkzeug.exceptions import BadRequest


class LeadAction(Resource):

    @login_required
    def get(self, action):
        # todo pagination
        user_id = current_user.get_id()
        user_type = current_user.get_type()
        leads = LeadRepository().get_lead_by_action(action, user_id, user_type)
        result = []
        if leads:
            for lead in leads:
                result.append(LeadOutputAdapter().parse(lead))
            return result
        raise BadRequest("No leads found")



