from app.extensions import db
from sqlalchemy.orm import backref
from app.models.product import Product
from app.models.image import Image

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description  = db.Column(db.String(200))
    cat_img = db.Column(db.String(), nullable=True)
    slug = db.Column(db.String(), nullable=False, unique=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
    children = db.relationship('Category', backref=backref('parent', remote_side=[id]), lazy=True)
    products = db.relationship('Product', backref='theCategory', lazy=True)
        
    def __repr__(self):
        return f'<Cat ID: {self.id}, name: {self.name}, parent: {self.parent_id}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def totalProducts(self):
        ''' Returns the Total Number of products in category '''
        
        numProducts = len(Product.query.filter(Product.category_id == self.id).all())
        return numProducts
    
    def format(self):
        numProducts = len(Product.query.filter(Product.category_id == self.id).all())
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat_img': self.cat_img,
            'slug': self.slug,
            'totalProducts': numProducts
            }

    def getThumbImage(self):
        theImage = Image.query.get(self.cat_img)
        if theImage:
            return theImage.get_path("thumb")
        else:
            return None
    
    def getMediumImage(self):
        theImage = Image.query.get(self.cat_img)
        if theImage:
            return theImage.get_path("medium")
        else:
            return None

    def getLargeImage(self):
        theImage = Image.query.get(self.cat_img)
        if theImage:
            return theImage.get_path("large")
        else:
            return None
