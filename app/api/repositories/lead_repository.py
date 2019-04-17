from app.api.adapters.InputAdapters import LeadInputAdapter
from app.api.models import User, Lead
from werkzeug.exceptions import BadRequest
from app import db


class LeadRepository(object):

    def add_lead(self, parsed_lead, user_id, user_type):
        lead = Lead()
        if db.session.query(User).filter(User.id == user_id and User.type == user_type).first():
            lead.user_id = user_id
            if parsed_lead[LeadInputAdapter.TITLE]:
                lead.title = parsed_lead[LeadInputAdapter.TITLE]
            if parsed_lead[LeadInputAdapter.LEAD_DESCRIPTION]:
                lead.lead_description = parsed_lead[LeadInputAdapter.LEAD_DESCRIPTION]
            if parsed_lead[LeadInputAdapter.SUBCATEGORY]:
                lead.sub_category = parsed_lead[LeadInputAdapter.SUBCATEGORY]
            if parsed_lead[LeadInputAdapter.CATEGORY]:
                lead.category = parsed_lead[LeadInputAdapter.CATEGORY]
            if parsed_lead[LeadInputAdapter.PRICE]:
                lead.price = parsed_lead[LeadInputAdapter.PRICE]
            try:
                db.session.add(lead)
                db.session.commit()
            except:
                db.session.rollback()
            return lead
        raise BadRequest("error in adding lead ")

    def get_lead_by_user_id(self, user_id, user_type):
        #todo limit and offset
        user = db.session.query(User).filter(User.id == user_id, User.type == user_type).first()
        if user.type == int(User.TYPE['admin']) or user.type == int(User.TYPE['super_admin']):
            leads = db.session.query(Lead).all() #todo distribute leads to different admin
            lead_details = []
            if leads:
                for lead in leads:
                    lead_details.append(lead)
                return lead_details
        if user.type == int(User.TYPE['user']):
            leads = db.session.query(Lead).filter(Lead.user_id == user_id, Lead.status == Lead.APPROVED).all() #todo limit and offset
            lead_details = []
            if leads:
                for lead in leads:
                    lead_details.append(lead)
                return lead_details
        raise BadRequest("No lead available")

    def approve_lead(self, lead_id, user_type):
        if user_type == User.TYPE['super_admin'] and user_type == User.TYPE['admin']:
            lead = db.session.query(Lead).filter(Lead.id == lead_id).first()
            if lead:
                lead.status = Lead.APPROVED
                try:
                    db.session.add(lead)
                    db.session.commit()
                except:
                    db.session.rollback()
                return lead
            raise BadRequest("Lead Not Available")
        return None

    def get_lead_by_lead_id(self, lead_id, user_type):
        if user_type == int(User.TYPE['admin']) and user_type == int(User.TYPE['super_admin']):
            lead = db.session.query(Lead).filter(Lead.id == lead_id).first()
            return lead
        else: 
            lead = db.session.query(Lead).filter(Lead.id == lead_id, Lead.status == Lead.APPROVED).first()
            return lead
        
    def update_lead(self, parsed_lead, lead_id, user_id, user_type):
        lead = db.session.query(Lead).filter(Lead.id == lead_id).first()
        lead.title = parsed_lead[LeadInputAdapter.TITLE]
        lead.lead_description = parsed_lead[LeadInputAdapter.LEAD_DESCRIPTION]
        lead.sub_category = parsed_lead[LeadInputAdapter.SUBCATEGORY]
        lead.category = parsed_lead[LeadInputAdapter.CATEGORY]
        if lead and user_type == int(User.TYPE['user']) and user_id == lead.user_id:
            # user can edit title, lead_description, subcategory, category after submitting lead
            try:
                db.session.add(lead)
                db.session.commit()
            except:
                db.session.rollback()
            return lead
        if lead and (user_type == int(User.TYPE['super_admin']) or user_type == int(User.TYPE['admin'])):
            # admin and super admin can also edit tag, price, score, features
            lead.price = parsed_lead[LeadInputAdapter.PRICE]
            lead.tag = parsed_lead[LeadInputAdapter.TAG]
            lead.score = parsed_lead[LeadInputAdapter.SCORE]
            lead.features = parsed_lead[LeadInputAdapter.FEATURES]
            try:
                db.session.add(lead)
                db.session.commit()
            except:
                db.session.rollback()
            return lead
        raise BadRequest("Lead not found")







