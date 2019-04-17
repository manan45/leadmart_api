from flask_restful import reqparse


class OtpInputAdapter():

    MOBILE = 'mobile'
    OTP = 'otp'

    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.MOBILE, required=True, type=str)
        parser.add_argument(self.OTP, required=False, type=str)
        return parser.parse_args()


