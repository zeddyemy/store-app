from functools import wraps
from flask_login import LoginManager, login_required, current_user
from flask import current_app, request, redirect, flash, url_for, render_template
from app.models.role import Role
from app.appfunctions import redirect_url


def roles_required(*perms):
    """
    use this decorator by passing a role string.
    If you decorate a view with this, it will ensure that the current user has a particular role
    before calling the actual view. (If they don't have the given role,
    i.e the role string passed into the decorator,
    it will redirect them to the previous page)
    For example::
        @app.route('/post')
            @roles_required('admin', 'customer')
            def post():
                pass
    
    """
    def decorator(func):
        @wraps(func)
        def wrapper_decorator(*args, **kwargs):
            userRoleId = current_user.role_id
            getRole = Role.query.filter(Role.id == userRoleId).first()
            currentUserRole = getRole.name
            
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            elif currentUserRole == 'customer':
                page='error'
                return render_template('frontend/errors/permission.html', page=page)
            elif not currentUserRole in perms:
                page='error'
                return render_template('cpanel/errors/permission.html', page=page)
            
            return func(*args, **kwargs)
                
        return wrapper_decorator
    return decorator

def frontendLogin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        next=request.path
        if not current_user.is_authenticated:
            flash("You need to login first", 'error')
            return redirect(url_for('frontend.login', next=request.path))

        return func(*args, **kwargs)

    return decorated_view