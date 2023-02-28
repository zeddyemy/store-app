from random import choices
from wsgiref.validate import validator
import phonenumbers
from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, TextAreaField, EmailField, PasswordField, SelectField, SelectMultipleField, BooleanField, HiddenField, ValidationError, widgets)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, Optional, Email, Regexp
from sqlalchemy import desc

from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.person import Person
from app.appfunctions import getRoleNames

def cat_query():
    queryCategories = db.session.query(Category.name).order_by(desc('id')).all()
    allCategories = ['-- Select --',]
    
    for cat in queryCategories:
        allCategories.append(cat.name)
    
    print("\n\n", allCategories)
    return allCategories

choices = [
    'XS',
    'S',
    'M',
    'L',
    'XL',
    'XXL',
    '2XL',
    '3XL',
    '4XL',
    '35',
    '36',
    '37',
    '39',
    '40',
    '41',
    '42',
    '43',
    '44',
    '45',
    '46',
    '50',
]

# class to change the way SelectMultipleField
# is rendered by jinja
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# form to add new category
class CategoryForm(FlaskForm):
    name = StringField(
        'name', validators=[InputRequired(), Length(min=1, max=30)])
    description = TextAreaField(
        'description'
    )
    parent_cat = SelectField(
        'parent_cat',
        choices=cat_query,
        validate_choice=False
    )
    cat_img = FileField(
        'Category Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])

# form to add new product
class ProductForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    description = TextAreaField(
        'description', validators=[Optional()]
    )
    sellingPrice = IntegerField(
        'sellingPrice', validators=[DataRequired()]
    )
    actualPrice = IntegerField(
        'actualPrice', validators=[Optional()]
    )
    
    global choices
    selectAvailableSizes = MultiCheckboxField(
        'sizes', choices=choices, validators=[Optional()])
    
    colors = StringField(
        'colors', validators=[Optional()]
    )
    productCat = SelectField(
        'productCat',
        choices=cat_query,
        validate_choice=False
    )
    product_img = FileField(
        'Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])

# form to add new user
class SignUpForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            )
        ]
    )
    email = EmailField(
        'Email address', validators=[DataRequired(), Email(), Length(1, 64)]
    )
    firstname = StringField(
        'First Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    lastname = StringField(
        'Last Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(4, 72),
            EqualTo('confirmPasswd', message='Passwords Must Match!')
        ]
    )
    confirmPasswd = PasswordField(
        'Confirm Password', validators=[
            DataRequired(),
            Length(4, 72),
            EqualTo('password', message='Passwords Must Match!')
        ]
    )
    
    def validate_email(self, email):
        if Person.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if Person.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")

# form for user to login
class LoginForm(FlaskForm):
    emailUsername = StringField(
        'Email address', validators=[DataRequired(), Length(1, 64)]
    )
    pwd = PasswordField(
        'Password', validators=[
            DataRequired(), Length(min=4, max=72)
        ]
    )

# form for the admin to add new user of the dashboard
class adminUsersForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired()]
    )
    email = EmailField(
        'Email address', validators=[DataRequired(), Email()]
    )
    firstname = StringField(
        'First Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    lastname = StringField(
        'Last Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    
    password = PasswordField(
        'Password', validators=[DataRequired(), EqualTo('confirmPasswd', message='Passwords Must Match!')]
    )
    confirmPasswd = PasswordField(
        'Confirm Password', validators=[DataRequired()]
    )
    role = SelectField(
        'role',
        choices=getRoleNames,
        validate_choice=False
    )
    existingEmail = HiddenField()
    existingUsername = HiddenField()
    
    def validate_email(self, email):
        if Person.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if Person.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")

# form for the admin to edit user of the dashboard
class adminEditUserForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired()]
    )
    email = EmailField(
        'Email address', validators=[DataRequired(), Email()]
    )
    role = SelectField(
        'role',
        choices=getRoleNames,
        validate_choice=False
    )
    existingEmail = HiddenField()
    existingUsername = HiddenField()

# form to edit user profile
class editProfileForm(FlaskForm):
    profilePic = FileField(
        'Profile Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    
    firstname = StringField(
        'First Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    lastname = StringField(
        'Last Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            )
        ]
    )
    email = EmailField(
        'Email address', validators=[DataRequired(), Email(), Length(1, 64)]
    )
    
    phone = StringField(
        'Phone Number', validators=[DataRequired()]
    )
    
    country = StringField(
        'Country', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid Country"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you provided a correct country",
            )
        ]
    )
    state = StringField(
        'State', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you provided a correct state",
            )
        ]
    )
    city = StringField(
        'City', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you provided a correct city",
            )
        ]
    )
    postalCode = IntegerField(
        'Postal Code', validators=[DataRequired()]
    )
    defaultAddress = StringField(
        'Address', validators=[DataRequired()]
    )
    
    
    def validate_phone(self, phoneNumber):
        try:
            p = phonenumbers.parse(phoneNumber.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')