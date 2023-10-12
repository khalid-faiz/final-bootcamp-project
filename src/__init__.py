from decouple import config
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registering blueprints
from src.index.views import index_bp
from src.user.views import user_bp

app.register_blueprint(index_bp)
app.register_blueprint(user_bp, url_prefix="/user")