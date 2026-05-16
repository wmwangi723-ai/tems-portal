import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tems.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # SECURITY: Pull secret key from environment, fallback for local dev
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')
    
    # SECURITY: Limit file uploads to 5MB maximum to prevent server crashes
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 
    
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models
        from .main_routes import main_bp
        app.register_blueprint(main_bp)

    return app