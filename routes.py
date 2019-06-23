from app.api import resources

endpoints = [
    (resources.Register, '/register'),
    (resources.SendOtp, '/send_otp'),
    (resources.VerifyOtp, '/verify_otp'),
    (resources.Login, '/login'),
    (resources.Logout, '/logout'),
    (resources.UserId, '/user/<user_id>'),
    (resources.Lead, '/leads'),
    (resources.ApproveLead, '/<lead_id>/APPROVE'),
    (resources.RejectLead, '/<lead_id>/REJECT'),
    (resources.LeadId, '/leads/<lead_id>'),
    (resources.LeadAction, '/lead/<action>'),
    (resources.Users, '/users/<type>'),
    (resources.UserAction, '/action/<action>/<user_id>'),
    (resources.RemoveAdmin, '/<demote>/DEMOTE'),
    (resources.MakeAdmin, '/<promote>/PROMOTE'),
    (resources.AdminLeads, '/admin/leads/<action>')

]
