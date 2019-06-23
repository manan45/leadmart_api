from werkzeug.exceptions import BadRequest, Unauthorized
from app import db
from app.api.adapters.InputAdapters import UserInputAdapter, OtpInputAdapter,LoginInputAdapter
from app.api.models import User, OTP, UserLogin
from app.api.lib import StaticUtils
import jwt, json, datetime, random, re, time
from config import env
import requests


class UserRepository(object):
    def add_user(self, parsed_user):
        user = User()
        if self.check_user_name(parsed_user[UserInputAdapter.NAME]):
            user.name = parsed_user[UserInputAdapter.NAME]
        if self.validate_user_password(parsed_user[UserInputAdapter.PASSWORD]) == self.validate_user_password(parsed_user[UserInputAdapter.CONFIRM_PASSWORD]):
            user.password = parsed_user[UserInputAdapter.PASSWORD]
        else:
            raise BadRequest('Password do not match')
        if self.check_email(parsed_user[UserInputAdapter.EMAIL]):
            user.email = parsed_user[UserInputAdapter.EMAIL]
        if self.check_mobile(parsed_user[UserInputAdapter.MOBILE]):
            mobile = parsed_user[UserInputAdapter.MOBILE]
            user.mobile = StaticUtils.validate_mobile(mobile)

        user.username = self.get_unique_username_from_name(parsed_user[UserInputAdapter.NAME])

        if self.validate_user_password(user.password):
            user.password = StaticUtils.create_password_hash(user.password)

        if user.email:
            self.check_if_email_exists(user.email)

        if user.username:
            self.check_if_username_exists(user.username)

        if user.mobile:
            self.check_if_mobile_exists(user.mobile)

        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

        return user

    def verify_otp(self, parsed_otp):
        mobile = parsed_otp[OtpInputAdapter.MOBILE]
        otp = parsed_otp[OtpInputAdapter.OTP]
        otp_details = db.session.query(OTP).filter(OTP.mobile == mobile, OTP.is_verified == OTP.IS_VERIFIED_FALSE, OTP.otp == otp).first()
        if otp_details:
            otp_details.is_verified = OTP.IS_VERIFIED_TRUE
            try:
                db.session.add(otp_details)
                db.session.commit()
            except:
                db.session.rollback()
            return otp_details
        raise BadRequest('Otp not valid')

    def encode_auth_token(self, user):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': json.dumps({'type': user.type, 'email': user.email, 'user_id': user.id, 'username': user.username, 'is_active': UserLogin.IS_ACTIVE_TRUE})

            }
            return jwt.encode(payload, env['SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, env['SECRET_KEY'])
            return json.loads(payload['sub'])
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def sendPostRequest(self, reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
        req_params = {
            'apikey': apiKey,
            'secret': secretKey,
            'usetype': useType,
            'phone': phoneNo,
            'message': textMessage,
            'senderid': senderId
        }
        return requests.post(reqUrl, req_params)

    def send_otp(self, parsed_otp):  # parsed mobile
        otp = OTP()
        generated_otp = self.generate_otp()

        if self.check_mobile(parsed_otp[OtpInputAdapter.MOBILE]):
            otp.mobile = parsed_otp[OtpInputAdapter.MOBILE]
            otp.is_verified = OTP.IS_VERIFIED_FALSE
            otp.otp = generated_otp
            try:
                db.session.add(otp)
                db.session.commit()
            except:
                db.session.rollback()
            return otp
        raise BadRequest("Failed to send otp")

    def generate_otp(self):
        otp = random.randint(0, 9999)
        return otp

    def get_unique_username_from_name(self, name):
        # if name does not exist in db in username field then make that as a username
        name = StaticUtils.make_alpha_numeric_string(name)
        try:
            self.check_if_username_exists(name)
            return name
        except BadRequest:
            return name + '-' + str(int(time.time()))

    def login(self, parsed_login):
        if self.check_argument(parsed_login[LoginInputAdapter.PASSWORD]):
            user_login = UserLogin()
            password = self.validate_user_password(parsed_login[LoginInputAdapter.PASSWORD])
            mobile = StaticUtils.validate_mobile(parsed_login[LoginInputAdapter.MOBILE])
            if password and mobile:
                hashed_password = StaticUtils.create_password_hash(password)
                user = db.session.query(User).filter(User.mobile == mobile, User.password == hashed_password, User.is_blocked == User.IS_BLOCKED_FALSE).first()
                if user:
                    user_login.user_id = user.id
                    user_login.is_active = UserLogin.IS_ACTIVE_TRUE
                    user_login.token = self.encode_auth_token(user)
                    user_login.user_type = user.type
                    try:
                        db.session.add(user_login)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    return user_login
                raise BadRequest("User is blocked")
            raise BadRequest("Mobile or password incorrect")
        elif self.check_argument(parsed_login[LoginInputAdapter.OTP]):
            user_login = UserLogin()
            mobile = StaticUtils.validate_mobile(parsed_login[LoginInputAdapter.MOBILE])
            otp_details = db.session.query(OTP).filter(OTP.mobile == mobile, OTP.otp == parsed_login[LoginInputAdapter.OTP],
                                                                                OTP.is_verified == OTP.IS_VERIFIED_TRUE).first()
            if otp_details and mobile:
                user = db.session.query(User).filter(User.mobile == parsed_login[LoginInputAdapter.MOBILE], User.is_blocked == User.IS_BLOCKED_FALSE).first()
                if user:
                    user_login.user_id = self.get_user_from_mobile(parsed_login[LoginInputAdapter.MOBILE])
                    user_login.token = self.encode_auth_token(user)
                    user_login.is_active = UserLogin.IS_ACTIVE_TRUE
                    user_login.user_type = user.type
                    try:
                        db.session.add(user_login)
                        db.session.commit()
                    except:
                        db.session.rollback()
                    return user_login
                raise BadRequest("user is blocked")
            raise BadRequest("Otp or Mobile is incorrect")
        raise BadRequest("error occurred")

    def logout(self, user_id):
        logged_user = db.session.query(UserLogin).filter(UserLogin.user_id == user_id, UserLogin.is_active == UserLogin.IS_ACTIVE_TRUE).first()
        if logged_user:
            logged_user.is_active = UserLogin.IS_ACTIVE_FALSE
            try:
                db.session.add(logged_user)
                db.session.commit()
            except:
                db.session.rollback()
            return logged_user
        raise BadRequest('Error')

    def get_user(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            return user
        raise BadRequest('Error')

    def update_user(self, parsed_user, user_id):
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            email = parsed_user[UserInputAdapter.EMAIL] if parsed_user[UserInputAdapter.EMAIL] else None
            if email and user.email != email and not self.check_if_email_exists(email):
                user.email = email
            mobile = parsed_user[UserInputAdapter.MOBILE] if parsed_user[UserInputAdapter.MOBILE] else None
            if mobile and user.mobile != mobile and not self.check_if_mobile_exists(mobile):
                user.mobile = mobile
            if parsed_user[UserInputAdapter.SURNAME]:
                user.surname = parsed_user[UserInputAdapter.SURNAME]
            if parsed_user[UserInputAdapter.NAME]:
                user.name = parsed_user[UserInputAdapter.NAME]
            if parsed_user[UserInputAdapter.COUNTRY]:
                user.country = parsed_user[UserInputAdapter.COUNTRY]
            if parsed_user[UserInputAdapter.STATE]:
                user.state = parsed_user[UserInputAdapter.STATE]
            if parsed_user[UserInputAdapter.ADDRESS]:
                user.address = parsed_user[UserInputAdapter.ADDRESS]
            if parsed_user[UserInputAdapter.TWITTER]:
                user.twitter = parsed_user[UserInputAdapter.TWITTER]
            if parsed_user[UserInputAdapter.INSTAGRAM]:
                user.instagram = parsed_user[UserInputAdapter.INSTAGRAM]
            if parsed_user[UserInputAdapter.LINKEDIN]:
                user.linkedin = parsed_user[UserInputAdapter.LINKEDIN]
            if parsed_user[UserInputAdapter.DESIGNATION]:
                user.designation = parsed_user[UserInputAdapter.DESIGNATION]
            if parsed_user[UserInputAdapter.COMPANY_NAME]:
                user.company_name = parsed_user[UserInputAdapter.COMPANY_NAME]

            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
            return user
        return None

    def get_user_from_mobile(self, mobile):
        user_details = db.session.query(User).filter(User.mobile == mobile).first()
        if user_details:
            return user_details.id
        return None

    def check_if_username_exists(self, username):
        if db.session.query(User).filter(User.username == username).first():
            raise BadRequest("Username is already taken")
        return None

    def check_if_email_exists(self, email):
        if not StaticUtils.validate_email(email):
            raise BadRequest('email is bot valid')
        if db.session.query(User).filter(User.email == email).first():
            raise BadRequest('This email is already registered')
        return None

    def check_if_mobile_exists(self, mobile):
        if not StaticUtils.validate_mobile(mobile):
            raise BadRequest('Enter a valid mobile number')
        if db.session.query(User).filter(User.mobile == mobile).first():
            raise BadRequest('mobile number is already registered')
        return None

    @staticmethod
    def check_mobile(mobile):
        if mobile:
            return mobile
        raise BadRequest('Mobile number is required')

    @staticmethod
    def check_user_name(name):
        if name:
            name = name.lower()
            if name.isalpha():
                return name
            raise BadRequest('Name is not Valid')
        raise BadRequest('Name is required')

    @staticmethod
    def check_email(email):
        if email:
            return email
        raise BadRequest('Email is required')

    @staticmethod
    def validate_user_password(password):
        while True:
            if len(password) < 8:
                raise BadRequest("password length is less than 8")
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            else:
                return password
        if flag == -1:
            raise BadRequest('use the correct format for password')

    @staticmethod
    def check_argument(args):
        if args:
            return True
        return False
