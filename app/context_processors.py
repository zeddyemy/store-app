from flask_login import current_user

from app.appfunctions import getUserInfo
from app.help_functions.cart_methods import getCartCount
from app.extensions import db

def myContextProcessor():
    if current_user.is_authenticated:
        current_user_obj = db.session.merge(current_user)
        db.session.remove()
        userId = current_user_obj.id
    else:
        userId = None
    
    userInfo = getUserInfo(userId)
    cart_count = getCartCount()
    
    return {'CURRENT_USER': userInfo, 'CART_COUNT': cart_count}