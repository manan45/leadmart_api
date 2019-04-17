from flask_sqlalchemy import SQLAlchemy
from config import env


class MYSQL():

    def load(self, app):
        app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqldb://' + env['db_user']+':' + env['db_password'] \
                                                + '@' + env['db_host'] + '/' + env['db_name']

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['SQLALCHEMY_POOL_SIZE'] = 100
        app.config['SQLALCHEMY_POOL_RECYCLE'] = 900
        return SQLAlchemy(app)
