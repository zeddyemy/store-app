from flask import Blueprint

bp = Blueprint('ctrlPanel', __name__)

from app.ctrl_panel import routes
from app.ctrl_panel import auth_routes
from app.ctrl_panel import categories_routes
from app.ctrl_panel import products_routes
from app.ctrl_panel import users_routes
