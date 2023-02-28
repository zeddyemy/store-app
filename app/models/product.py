from flask import request
from sqlalchemy.orm import backref
from datetime import datetime

from app.extensions import db
from app.models.image import Image

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description  = db.Column(db.String(300), nullable=True)
    sellingPrice = db.Column(db.Integer, nullable=False)
    actualPrice = db.Column(db.Integer, nullable=True)
    sizes = db.Column(db.String(300), nullable=True)
    colors = db.Column(db.String(), nullable=True)
    product_img = db.Column(db.String(), nullable=True)
    slug = db.Column(db.String(), nullable=False, unique=True)
    pubDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=True,)
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person', backref=db.backref('products', lazy='dynamic'))

    def __repr__(self):
        return f'<Product ID: {self.id}, name: {self.name}, catId: {self.category_id}'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def getThumbImage(self):
        theImage = Image.query.get(self.product_img)
        if theImage:
            return theImage.get_path("thumb")
        else:
            return None
    
    def getMediumImage(self):
        theImage = Image.query.get(self.product_img)
        if theImage:
            return theImage.get_path("medium")
        else:
            return None

    def getLargeImage(self):
        theImage = Image.query.get(self.product_img)
        if theImage:
            return theImage.get_path("large")
        else:
            return None

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sellingPrice': self.sellingPrice,
            'actualPrice': self.actualPrice,
            'sizes': self.sizes,
            'colors': self.colors,
            'product_img': self.getMediumImage(),
            'slug': self.slug,
            }