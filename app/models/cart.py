from app.extensions import db
from sqlalchemy.orm import backref
from datetime import datetime
from app.models.product import Product


cart_products = db.Table('cart_products',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, default=1)
)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    products = db.relationship('Product', secondary=cart_products, backref=db.backref('carts', lazy=True))
    cart_products = db.relationship('CartProduct', backref='cart', lazy=True)
    
    
    def addProduct(self, product, size='', color='', quantity=1):
        cart_product = CartProduct.query.filter_by(cart_id=self.id, product_id=product.id, size=size, color=color).first()
        if cart_product:
            cart_product.quantity += quantity
        else:
            cart_product = CartProduct(cart=self, product=product, quantity=quantity, size=size, color=color)
            db.session.add(cart_product)
        db.session.commit()

    def deleteProduct(self, product_id, size='', color=''):
        cart_product = CartProduct.query.filter_by(cart_id=self.id, product_id=product_id, size=size, color=color).first()
        if cart_product:
            db.session.delete(cart_product)
            db.session.commit()
    
    @property
    def cartCount(self):
        return sum(cart_product.quantity for cart_product in self.cart_products)

class CartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    size = db.Column(db.String(20))
    color = db.Column(db.String(20))
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref=db.backref('cart_products', lazy=True))