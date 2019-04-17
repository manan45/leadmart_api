from flask_restful import reqparse


class UserInputAdapter():

    NAME = 'name'
    SURNAME = 'surname'
    PASSWORD = 'password'
    CONFIRM_PASSWORD = 'confirm_password'
    EMAIL = 'email'
    MOBILE = 'mobile'
    COMPANY_NAME = 'company_name'
    DESIGNATION = 'designation'
    FACEBOOK = 'facebook'
    LINKEDIN = 'linkedin'
    INSTAGRAM = 'instagram'
    TWITTER = 'twitter'
    ADDRESS = 'address'
    CITY = 'city'
    STATE = 'state'
    COUNTRY = 'country'
    PROFILE = 'profile'

    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.PASSWORD, required=False, type=str)
        parser.add_argument(self.CONFIRM_PASSWORD, required=False, type=str)
        parser.add_argument(self.EMAIL, required=False, type=str)
        parser.add_argument(self.NAME, required=False, type=str)
        parser.add_argument(self.MOBILE, required=False, type=str)
        parser.add_argument(self.COMPANY_NAME, required=False, type=str)
        parser.add_argument(self.DESIGNATION, required=False, type=str)
        parser.add_argument(self.SURNAME, required=False, type=str)
        parser.add_argument(self.FACEBOOK, required=False, type=str)
        parser.add_argument(self.LINKEDIN, required=False, type=str)
        parser.add_argument(self.INSTAGRAM, required=False, type=str)
        parser.add_argument(self.TWITTER, required=False, type=str)
        parser.add_argument(self.ADDRESS, required=False, type=str)
        parser.add_argument(self.CITY, required=False, type=str)
        parser.add_argument(self.STATE, required=False, type=str)
        parser.add_argument(self.COUNTRY, required=False, type=str)
        parser.add_argument(self.PROFILE, required=False, type=str)
        return parser.parse_args()
