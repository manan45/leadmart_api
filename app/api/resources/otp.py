from flask_restful import Resource
from app.api.adapters.InputAdapters import OtpInputAdapter
from werkzeug.exceptions import BadRequest
from app.api.repositories import UserRepository


class SendOtp(Resource):

    def post(self):
        parsed_otp = OtpInputAdapter().parse()
        otp = UserRepository().send_otp(parsed_otp)
        if otp:
            return {
                "message": "otp sent",
                "otp": otp.otp
            }
        raise BadRequest("Error Occurred")


class VerifyOtp(Resource):

    def post(self):
        parsed_otp = OtpInputAdapter().parse()
        if UserRepository().verify_otp(parsed_otp):
            return {
                "message": "otp is verified"
            }
        raise BadRequest('Error Occurred')
