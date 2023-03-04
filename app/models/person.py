from app.extensions import db
from sqlalchemy.orm import backref
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.role import Role
from app.models.image import Image

# Define the User data model. Make sure to add flask_login UserMixin!!
class Person(db.Model, UserMixin):
    __tablename__ = "person"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    thePassword = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(), nullable=False, unique=True)
    dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), nullable=False,)
    role = db.relationship('Role')
    profile = db.relationship('Profile', back_populates="person", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="person", uselist=False, cascade="all, delete-orphan")
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.thePassword = generate_password_hash(password)
    
    def verify_password(self, password):
        '''
        #This returns True if the form password is same as hashed password in the database.
        '''
        return check_password_hash(self.thePassword, password)
    
    def getRoleName(self, id):
        role = Role.query.filter(Role.id == self.role_id).first()
        return role.name
    
    def __repr__(self):
        return f'<ID: {self.id}, username: {self.username}, email: {self.email},'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Profile(db.Model):
    __tablename__ = "profile"
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(200), nullable=True)
    lastname = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    profilePic = db.Column(db.String(), nullable=True)
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False,)
    person = db.relationship('Person', back_populates="profile")
    
    def __repr__(self):
        return f'<profile ID: {self.id}, name: {self.firstname}, person ID: {self.person_id}>'
    
    def getThumbImage(self):
        theImage = Image.query.get(self.profilePic)
        if theImage:
            return theImage.get_path("thumb")
        else:
            return None
    
    def getMediumImage(self):
        theImage = Image.query.get(self.profilePic)
        if theImage:
            return theImage.get_path("medium")
        else:
            return None

    def getLargeImage(self):
        theImage = Image.query.get(self.profilePic)
        if theImage:
            return theImage.get_path("large")
        else:
            return None


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    postalCode = db.Column(db.Integer(), nullable=True)
    
    defaultAddress = db.Column(db.String(100), nullable=True)
    otherAddresses = db.Column(db.String(100), nullable=True)
    
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False,)
    person = db.relationship('Person', back_populates="address")

