import sys
import json
from flask import render_template, request, Response, flash, redirect, url_for, jsonify, make_response, abort
from flask_login import login_user, current_user
from app.frontend import bp
from app.extensions import db
from app.models.product import Product
from app.models.cart import Cart, CartProduct
from app.models.person import Person
from app.appfunctions import getAllProducts, get_or_404
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
        
        quantity = int(request.form.get('quantity', 1))
    
        # Check if user is logged in
        if current_user.is_authenticated:
            # Add the product to the user's cart
            cart = Cart.query.filter_by(person_id=current_user.id).first()
            if not cart:
                cart = Cart(person_id=current_user.id)
                db.session.add(cart)
                db.session.commit()
            
            cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product.id).first()
            if cart_product:
                cart_product.quantity += quantity
            else:
                cart_product = CartProduct(cart_id=cart.id, product_id=product.id, quantity=quantity)
                db.session.add(cart_product)
            
            db.session.commit()
            cart_count = sum(cart_product.quantity for cart_product in cart.cart_products)
            resp_data = {'success': True, 'cart_count': cart_count}
            resp = jsonify(resp_data)
        else:
            # Add the product to the cart stored in the cookie
            cart_items = request.cookies.get('cart_items')
            if cart_items:
                cart_items = json.loads(cart_items)
            else:
                cart_items = []
            
            updated_cart_items = False
            for item in cart_items:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    updated_cart_items = True
                    break
            
            if not updated_cart_items:
                cart_items.append({'product_id': product_id, 'quantity': quantity})
            
            cart_count = sum(item['quantity'] for item in cart_items)
            resp_data = {'success': True, 'cart_count': cart_count}
            resp = jsonify(resp_data)
            resp.set_cookie('cart_items', json.dumps(cart_items))
    except Exception as e:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        print('An error occurred. ')
        # handle exceptions by returning an error response
        return jsonify({'success': False, 'error': str(e)})
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
            products.append((product, cart_product.quantity))
    else:
        getCartItems = request.cookies.get('cart_items')
        if getCartItems:
            cart_items = json.loads(getCartItems)
        else:
            cart_items = []
        
        for cart_item in cart_items:
            product = Product.query.filter_by(id=cart_item['product_id']).first()
            products.append((product, cart_item['quantity']))
    
    print("\n--------->>\n", products, "\n<<---------\n")

    return render_template('frontend/webpages/cart.html', page=page, products=products)
