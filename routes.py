from app.api import resources

endpoints = [
    (resources.User, '/register'),
    (resources.SendOtp, '/send_otp'),
    (resources.VerifyOtp, '/verify_otp'),
    (resources.Login, '/login'),
    (resources.Logout, '/logout'),
    (resources.UserId, '/user/<user_id>'),
    (resources.Lead, '/leads'),
    (resources.ApproveLead, '/<lead_id>/APPROVE'),
    (resources.RejectLead, '/<lead_id>/REJECT'),
    (resources.LeadId, '/leads/<lead_id>'),
    (resources.LeadAction, '/leads/<action>')

]
