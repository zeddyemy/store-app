from flask import Flask, render_template
from app.error_handlers import bp
from app.appfunctions import urlParts

@bp.app_errorhandler(404)
def not_found_error(error):
    if 'cpanel' in urlParts():
        return render_template('cpanel/errors/404.html', page='error'), 404
    else:
        return render_template('frontend/errors/404.html', page='error'), 404
    
@bp.app_errorhandler(422)
def unprocessable_error(error):
    if 'cpanel' in urlParts():
        return render_template('cpanel/errors/422.html', page='error'), 422
    else:
        return render_template('frontend/errors/422.html', page='error'), 422

@bp.app_errorhandler(500)
def server_error(error):
    if 'cpanel' in urlParts():
        return render_template('cpanel/errors/500.html', page='error'), 500
    else:
        return render_template('frontend/errors/500.html', page='error'), 500