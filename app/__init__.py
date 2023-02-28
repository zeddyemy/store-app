import os
import pathlib
from datetime import date
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate # Imported Migrate from flask_migrate.
from flask_login import LoginManager
from app.models.person import Person
from app.appfunctions import urlParts

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
    
    
    #app.add_url_rule('/static/uploads/<path:filename>', endpoint='uploads', view_func=app.send_static_file)
    
    @app.route('/test/')
    def test_page():
        
        year = (str(date.today().year))
        month = (str(date.today().month).zfill(2))
        datePath = year + '/' + month
            
        print("\n------------>>\n", year, "\n<<-------------\n")
        print("\n------------>>\n", month, "\n<<-------------\n")
        print("\n------------>>\n", datePath, "\n<<-------------\n")
        
        pathlib.Path(Config.UPLOADS_DIR, year).mkdir(exist_ok=True)
        pathlib.Path(Config.UPLOADS_DIR, year, month).mkdir(exist_ok=True)
        
        '''
        if not os.path.exists(uploadsDirectory):
            os.mkdir(uploadsDirectory)
        if not os.path.exists(subDirectory):
            os.mkdir(subDirectory)
        '''
        
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app
