from app.api.adapters.InputAdapters import LeadInputAdapter
from app.api.models import User, Lead, LeadSales
from werkzeug.exceptions import BadRequest, Unauthorized
from app import db
from datetime import timedelta, datetime


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

    def get_leads(self):
        #todo limit and offset
        leads = db.session.query(Lead).filter(Lead.status == Lead.APPROVE, Lead.is_deleted == Lead.IS_DELETED_FALSE).all() #todo limit and offset
        lead_details = []
        if leads:
            for lead in leads:
                lead_details.append(lead)
            return lead_details
        raise BadRequest('No lead Found')

    def approve_lead(self, lead_id, user_type):
        if user_type == int(User.TYPE['super_admin']) or user_type == int(User.TYPE['admin']):
            lead = db.session.query(Lead).filter(Lead.id == lead_id, Lead.status == Lead.REJECT, Lead.is_deleted == Lead.IS_DELETED_FALSE).first()
            if lead:
                lead.status = Lead.APPROVE
                try:
                    db.session.add(lead)
                    db.session.commit()
                except:
                    db.session.rollback()
                return lead
            raise BadRequest("Lead Not Available")
        raise Unauthorized("You are not authorised to for this action")

    def reject_lead(self, lead_id, user_type):
        if user_type == int(User.TYPE['super_admin']) or user_type == int(User.TYPE['admin']):
            lead = db.session.query(Lead).filter(Lead.id == lead_id, Lead.status == Lead.APPROVE, Lead.is_deleted == Lead.IS_DELETED_FALSE).first()
            if lead:
                lead.status = Lead.REJECT
                try:
                    db.session.add(lead)
                    db.session.commit()
                except:
                    db.session.rollback()
                return lead
            raise BadRequest("Lead Not Available")
        raise Unauthorized("You are not authorised to for this action")

    def get_lead_by_lead_id(self, lead_id, user_type):
        if user_type == int(User.TYPE['admin']) and user_type == int(User.TYPE['super_admin']):
            lead = db.session.query(Lead).filter(Lead.id == lead_id).first()
            return lead
        else: 
            lead = db.session.query(Lead).filter(Lead.id == lead_id, Lead.status == Lead.APPROVE).first()
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

    def get_lead_by_action(self, action, user_id, user_type):
        if action == Lead.ACTIONS['rejected']:
            result = self.get_rejected_leads(user_type, user_id)
        elif action == Lead.ACTIONS['active']:
            result = self.get_active_leads(user_type, user_id)
        elif action == Lead.ACTIONS['dead']:
            result = self.get_dead_leads(user_type, user_id)
        elif action == Lead.ACTIONS['submitted']:
            result = self.get_submitted_leads(user_id)
        elif action == Lead.ACTIONS['sold']:
            result = self.get_sold_leads(user_id)
        elif action == Lead.ACTIONS['bought']:
            result = self.get_bought_leads(user_id)
        else:
            raise BadRequest('Action not Available')
        return result

    # todo pagination
    def get_rejected_leads(self, user_type, user_id):
        user = db.session.query(User).filter(User.id == user_id, User.type == user_type).first()
        if user.type == int(User.TYPE['admin']) or user.type == int(User.TYPE['super_admin']):
            rejected_leads = db.session.query(Lead).filter(Lead.status == Lead.REJECT).all()
            result = []
            if rejected_leads:
                for rejected_lead in rejected_leads:
                    result.append(rejected_lead)
                return result
        if user.type == int(User.TYPE['user']):
            rejected_leads = db.session.query(Lead).filter(Lead.status == Lead.REJECT, Lead.user_id == user_id).all()
            result = []
            if rejected_leads:
                for rejected_lead in rejected_leads:
                    result.append(rejected_lead)
                return result
        raise BadRequest("No Lead Found")

    # todo pagination
    def get_active_leads(self, user_type, user_id):
        user = db.session.query(User).filter(User.id == user_id, User.type == user_type).first()
        if user.type == int(User.TYPE['admin']) or user.type == int(User.TYPE['super_admin']):
            active_leads = db.session.query(Lead).filter(Lead.status == Lead.APPROVE).all()
            result = []
            if active_leads:
                for active_lead in active_leads:
                    result.append(active_lead)
                return result
        if user.type == int(User.TYPE['user']):
            active_leads = db.session.query(Lead).filter(Lead.status == Lead.APPROVE, Lead.user_id == user_id).all()
            result = []
            if active_leads:
                for active_lead in active_leads:
                    result.append(active_lead)
                return result
        raise BadRequest("No Lead Found")

    # todo pagination
    def get_dead_leads(self, user_type, user_id):
        user = db.session.query(User).filter(User.id == user_id, User.type == user_type).first()
        if user.type == int(User.TYPE['user']):
            dead_leads = db.session.query(Lead).filter(Lead.user_id == user_id).all()
            result = []
            if dead_leads:
                for dead_lead in dead_leads:
                    if datetime.now() >= dead_lead.created + timedelta(days=15):  # change the timings of the dead lead
                        result.append(dead_lead)
                return result
        raise BadRequest("No Lead Found")

    # todo pagination
    def get_submitted_leads(self, user_id):
        leads = db.session.query(Lead).filter(Lead.user_id == user_id).all()
        result = []
        if leads:
            for lead in leads:
                result.append(lead)
            return result
        raise BadRequest("No lead found")

    # todo pagination
    def get_sold_leads(self, user_id):
        leads = db.session.query(LeadSales).filter(LeadSales.seller_id == user_id).all()
        result = []
        if leads:
            for lead in leads:
                result.append(lead.lead)
            return result
        raise BadRequest("No lead Found")

    # todo pagination
    def get_bought_leads(self, user_id):
        leads = db.session.query(LeadSales).filter(LeadSales.buyer_id == user_id).all()
        result = []
        if leads:
            for lead in leads:
                result.append(lead.lead)
            return result
        raise BadRequest("No lead found")

    def delete_lead(self, user_id, user_type, lead_id):
        lead = db.session.query(Lead).filter(Lead.user_id == user_id, Lead.id == lead_id, Lead.is_deleted == Lead.IS_DELETED_FALSE).first()
        if lead and (user_type == int(User.TYPE['admin']) or user_type == int(User.TYPE['super_admin'])):
            lead.is_deleted = Lead.IS_DELETED_TRUE
            try:
                db.session.add(lead)
                db.session.commit()
            except:
                db.session.rollback()
            return lead
        elif user_type == int(User.TYPE['admin']) or user_type == int(User.TYPE['super_admin']):
            lead = db.session.query(Lead).filter(Lead.id == lead_id, Lead.is_deleted == Lead.IS_DELETED_FALSE).first()
            if lead:
                lead.is_deleted = Lead.IS_DELETED_TRUE
                try:
                    db.session.add(lead)
                    db.session.commit()
                except:
                    db.session.rollback()
                return lead
            raise BadRequest("No lead Found")
        elif user_type == int(User.TYPE['user']):
            lead = db.session.query(Lead).filter(Lead.user_id == user_id, Lead.id == lead_id,
                                                 Lead.is_deleted == Lead.IS_DELETED_FALSE).first()
            if lead:
                lead.is_deleted = Lead.IS_DELETED_TRUE
                try:
                    db.session.add(lead)
                    db.session.commit()
                except:
                    db.session.rollback()
                return lead
            raise BadRequest("No lead Found")
        raise BadRequest("Error in deleting the lead")












