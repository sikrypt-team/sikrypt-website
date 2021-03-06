from flask import *
from app.config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db,render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'
app.debug = True

from app import routes,models