from flask import Blueprint

bp = Blueprint('frontend', __name__)

from app.frontend import routes
from app.frontend import auth_routes
from app.frontend import cart_routes
