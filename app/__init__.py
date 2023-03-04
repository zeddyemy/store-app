from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate # Imported Migrate from flask_migrate.
from flask_login import LoginManager
from app.models.person import Person

from config import Config
from app.extensions import db
from app.context_processors import myContextProcessor

import collections
collections.Callable = collections.abc.Callable

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.context_processor(myContextProcessor)

    # Initialize Flask extensions here
    db.init_app(app) # changed from db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    #Login Configuration
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'ctrlPanel.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Person.query.get(int(user_id))

    # Register blueprints here
    from app.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp)
    
    from app.ctrl_panel import bp as controlPanel_bp
    app.register_blueprint(controlPanel_bp, url_prefix='/cpanel')
    
    from app.error_handlers import bp as errorHandler_bp
    app.register_blueprint(errorHandler_bp)
    
    
    @app.route('/test/')
    def test_page():
        
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app
