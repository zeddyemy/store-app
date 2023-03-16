import json
from datetime import datetime, timedelta
from flask import request, make_response
from flask_login import current_user

from app.extensions import db
from app.models.cart import Cart, CartProduct
from app.models.product import Product

def clear_cart_cookie():
    response = make_response('')
    response.set_cookie('cart_items', '', max_age=0, expires=0)
    return response

def sync_cart():
    # Synchronize the cart stored in the cookie with the one stored in the database
    if 'cart_items' in request.cookies:
        cart_items = json.loads(request.cookies.get('cart_items'))
        cart = Cart.query.filter_by(person_id=current_user.id).first()
        if not cart:
            cart = Cart(person_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
            
        for item in cart_items:
            cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=item['product_id']).first()
            if cart_product:
                cart_product.quantity += item['quantity']
            else:
                cart_product = CartProduct(cart_id=cart.id, product_id=item['product_id'], quantity=item['quantity'])
                db.session.add(cart_product)
        
        db.session.commit()
        # Clear the cart_items cookie
        return clear_cart_cookie()
    else:
        response = make_response('')
        return response

def getCartCount(userId=''):
    cart_count = 0
    if userId or current_user.is_authenticated:
        cart = Cart.query.filter_by(person_id=userId or current_user.id).first()
        if cart:
            cart_count = sum(cart_product.quantity for cart_product in cart.cart_products)
    else:
        getCartItems = request.cookies.get('cart_items')
        if getCartItems:
            cartItems = json.loads(getCartItems)
            cart_count = sum([item['quantity'] for item in cartItems])
    
    return cart_count

