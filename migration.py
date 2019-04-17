from flask_migrate import Migrate
from app import APP, db

migrate = Migrate(APP, db)

from app.api.models import *



