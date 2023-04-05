import sys
import json
from flask import render_template, request, Response, flash, jsonify
from flask_login import login_user, current_user
from app.frontend import bp
from app.extensions import db
from app.models.product import Product
from app.models.cart import Cart, CartProduct
from app.models.person import Person
from app.decorators import frontendLogin_required

# Add to Cart
@bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
# @frontendLogin_required
def addToCart(product_id):
    page = 'add to cart'
    error = False
    
    try:
        product = Product.query.get(product_id)
        if not product:
            # handle case where product doesn't exist
            return jsonify({'success': False})
        
        data = request.get_json()
        size = data.get('size')
        color = data.get('color')
        quantity = int(data.get('quantity', 1))
        
        # Check if user is logged in
        if current_user.is_authenticated:
            # Add the product to the user's cart
            cart = Cart.query.filter_by(person_id=current_user.id).first()
            if not cart:
                cart = Cart(person_id=current_user.id)
                db.session.add(cart)
                db.session.commit()
            
            cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product.id, size=size, color=color).first()
            if cart_product:
                cart_product.quantity += quantity
            else:
                cart_product = CartProduct(cart_id=cart.id, product_id=product.id, size=size, color=color, quantity=quantity)
                db.session.add(cart_product)
            
            db.session.commit()
            cart_count = sum(cart_product.quantity for cart_product in cart.cart_products)
            resp_data = {'success': True, 'cart_count': cart_count}
            resp = jsonify(resp_data)
        else:
            # Add the product to the cart stored in the cookie
            getCartItems = request.cookies.get('cart_items')
            if getCartItems:
                cartItems = json.loads(getCartItems)
            else:
                cartItems = []
            
            updated_cart_items = False
            for item in cartItems:
                if item['product_id'] == product_id and item['size'] == size and item['color'] == color:
                    item['quantity'] += quantity
                    updated_cart_items = True
                    break
            
            if not updated_cart_items:
                cartItems.append({'product_id': product_id, 'size': size, 'color': color, 'quantity': quantity})
            
            cart_count = sum(item['quantity'] for item in cartItems)
            resp_data = {'success': True, 'cart_count': cart_count}
            resp = jsonify(resp_data)
            resp.set_cookie('cart_items', json.dumps(cartItems))
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # handle exceptions by returning an error response
        print('An error occurred.')
        return jsonify({'success': False, 'error': 'error'})
    else:
        return resp


# Cart page
@bp.route("/cart")
# @frontendLogin_required
def cart():
    page = 'cart'
    products = []
    
    if current_user.is_authenticated:
        # Get the user's cart
        cart = Cart.query.filter_by(person_id=current_user.id).first()

        # Get the products in the user's cart
        if cart:
            cart_products = CartProduct.query.filter_by(cart_id=cart.id).all()
        else:
            cart_products = []

        # Get the details of each product in the cart
        for cart_product in cart_products:
            product = Product.query.filter_by(id=cart_product.product_id).first()
            products.append((product, cart_product.quantity, cart_product.size, cart_product.color))
    else:
        getCartItems = request.cookies.get('cart_items')
        if getCartItems:
            cartItems = json.loads(getCartItems)
        else:
            cartItems = []
        
        for cart_item in cartItems:
            product = Product.query.filter_by(id=cart_item['product_id']).first()
            products.append((product, cart_item['quantity'], cart_item['size'], cart_item['color']))

    return render_template('frontend/webpages/cart.html', page=page, products=products)
