import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    # For local development, use SQLite; for Vercel, use in-memory
    if os.environ.get("VERCEL"):
        database_url = "sqlite:///:memory:"
    else:
        import os
        db_dir = os.path.join(os.getcwd(), 'instance')
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'tds_virtual_ta.db')
        database_url = f"sqlite:///{db_path}"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
if not os.environ.get("VERCEL"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

# initialize the app with the extension
db.init_app(app)

# Import models and routes
import models
import routes
import api

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        # Initialize sample data
        from ai_assistant_simple import initialize_simple_data
        initialize_simple_data()
    except Exception as e:
        app.logger.error(f"Database initialization error: {e}")
