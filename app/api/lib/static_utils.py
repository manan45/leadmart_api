import re
import hashlib
from werkzeug.exceptions import BadRequest


class StaticUtils():
    @staticmethod
    def validate_email(email):
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$)", email):
            return True
        return False

    @staticmethod
    def validate_mobile(mobile):
        if len(mobile) is not 10:
            raise BadRequest("Mobile Number is not valid ")
        return mobile

    @staticmethod
    def create_password_hash(password):
        h = hashlib.md5(password.encode())
        return h.hexdigest()

    @staticmethod
    def make_alpha_numeric_string(username):
        return re.sub('[^a-zA-Z0-9]',"", username)

