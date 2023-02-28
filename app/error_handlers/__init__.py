from flask import Blueprint

bp = Blueprint('errorHandlers', __name__)

from app.error_handlers import handlers
