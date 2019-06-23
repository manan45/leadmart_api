from app.api.models import User, Lead
from app import db
from werkzeug.exceptions import BadRequest, Unauthorized


class AdminRepository(object):

    def view_users_for_admin(self,  user_type, type_of_user):
        if user_type == int(User.TYPE['admin']) or user_type == int(User.TYPE['super_admin']):
            peoples = []
            # todo
            if type_of_user == 'ADMINS':
                admins = db.session.query(User).filter(User.type == User.TYPE['admin'], User.is_blocked == User.IS_BLOCKED_FALSE).all()
                if admins:
                    for admin in admins:
                        peoples.append(admin)
                    return peoples
                raise BadRequest("No admin found")
            if type_of_user == 'USERS':
                users = db.session.query(User).filter(User.type == User.TYPE['user'], User.is_blocked == User.IS_BLOCKED_FALSE).all()
                if users:
                    for user in users:
                        peoples.append(user)
                    return peoples
                raise BadRequest("No user found")
            raise Unauthorized("only admin and super admin are allowed")
        raise BadRequest("Error")

    def action_on_user(self, user_id, user_type, action):
        if user_type == int(User.TYPE['super_admin']) or user_type == int(User.TYPE['admin']):
            if action == "BLOCK":
                blocked_user = db.session.query(User).filter(User.id == user_id, User.is_blocked == User.IS_BLOCKED_FALSE).first()
                if blocked_user:
                    blocked_user.is_blocked = User.IS_BLOCKED_TRUE
                    try:
                        db.session.add(blocked_user)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    return blocked_user
                raise BadRequest("No user found")
            if action == "UNBLOCK":
                blocked_user = db.session.query(User).filter(User.id == user_id,
                                                             User.is_blocked == User.IS_BLOCKED_TRUE).first()
                if blocked_user:
                    blocked_user.is_blocked = User.IS_BLOCKED_FALSE
                    try:
                        db.session.add(blocked_user)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    return blocked_user
                raise BadRequest("No user found")
        else:
            blocked_user = db.session.query(User).filter(User.id == user_id,
                                                         User.is_blocked == User.IS_BLOCKED_FALSE).first()
            if blocked_user:
                blocked_user.is_blocked = User.IS_BLOCKED_TRUE
                try:
                    db.session.add(blocked_user)
                    db.session.commit()
                except:
                    db.session.rollback()
                return blocked_user
            raise BadRequest("No user found")

    def demote_the_admin(self, user_type, demote):
        if user_type == int(User.TYPE['super_admin']):
            admin = db.session.query(User).filter(User.id == demote, User.type == User.TYPE['admin'], User.is_blocked == User.IS_BLOCKED_FALSE).first()
            if admin:
                admin.type = User.TYPE['user']
                try:
                    db.session.add(admin)
                    db.session.commit()
                except:
                    db.session.rollback()
                return admin
            raise BadRequest("Admin is not available")
        raise Unauthorized("You are not Authorised to access this url")

    def promote_the_user(self, user_type, promote):
        if user_type == int(User.TYPE['super_admin']):
            user = db.session.query(User).filter(User.id == promote, User.is_blocked == User.IS_BLOCKED_FALSE).first()
            if user:
                user.type = User.TYPE['admin']
                try:
                    db.session.add(user)
                    db.session.commit()
                except:
                    db.session.rollback()
                return user
            raise BadRequest("User is not available")
        raise Unauthorized("You are not Authorised to access this url")

    # todo pagination
    def get_leads_for_admin(self, user_id, user_type, action):
        if user_type == int(User.TYPE['admin']) or user_type == int(User.TYPE['super_admin']):
            results = []
            if action == "REJECTED":
                leads = db.session.query(Lead).filter(Lead.status == Lead.REJECT, Lead.user_id == user_id, Lead.is_deleted == Lead.IS_DELETED_FALSE).all()
                if leads:
                    for lead in leads:
                        results.append(lead)
                    return results
                raise BadRequest("No lead found")
            if action == "APPROVED":
                leads = db.session.query(Lead).filter(Lead.status == Lead.APPROVE, Lead.user_id == user_id,
                                                      Lead.is_deleted == Lead.IS_DELETED_FALSE).all()
                if leads:
                    for lead in leads:
                        results.append(lead)
                    return results
                raise BadRequest("No lead found")
        raise Unauthorized("Not authorised to  access the url")



