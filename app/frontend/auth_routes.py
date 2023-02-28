import sys
from werkzeug.urls import url_parse
from flask import render_template, request, Response, flash, redirect, url_for, abort, make_response
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError )
from app.frontend import bp
from app.extensions import db
from app.appfunctions import redirect_url, verifyAndLogin
from app.help_functions.cart_methods import sync_cart
from app.models.category import Category
from app.models.product import Product
from app.models.person import Person
from app.models.role import Role
from app.forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


## Route to sign up user
@bp.route("/signup", methods=['GET', 'POST'])
def signUp():
    error = False
    form = SignUpForm()
    page = 'auth'
    
    if current_user.is_authenticated:
        return redirect(redirect_url('frontend.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print('------ {0}'.format(request.form))
            try:
                username = form.username.data
                email = form.email.data
                password = form.password.data
                
                hashedPw = generate_password_hash(password, "sha256")
                clientRole = Role.query.filter(Role.name=='customer').first()
                clientRoleId = clientRole.id
                
                newPerson = Person(username=username, email=email, thePassword=hashedPw, role_id=clientRoleId)
                db.session.add(newPerson)
                db.session.commit()
            except InvalidRequestError:
                db.session.rollback()
                flash(f"Something went wrong!", "danger")
            except IntegrityError:
                db.session.rollback()
                flash(f"User already exists!.", "warning")
            except DataError:
                db.session.rollback()
                flash(f"Invalid Entry", "warning")
            except DatabaseError:
                db.session.rollback()
                flash(f"Error connecting to the database", "danger")
            except Exception as e:
                error = True
                errMsg = e
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            if error:
                # on unsuccessful db insert, flash an error instead.
                flash(errMsg + ' - Please Try Again!', "error")
                print("\n\n there was an error ", username )
                abort(500)
            else:
                # on successful db insert, flash success
                flash('You account have been successfully created', 'success')
                return redirect(redirect_url('frontend.login'))
        else:
            allFields = ['email', 'username', 'password', 'confirmPasswd']
            if any(field in form.errors for field in allFields):
                pass
            else:
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        if fieldName == "csrf_token":
                            theErrMsg = "Sorry, we could not create your account. Please Try Again."
                            flash(theErrMsg, 'error')
                            print("\n------->>\n", err, "\n<<-------\n")
                            break
    
    return render_template('frontend/auth/sign_up.html', form=form, page=page)

## Route to Login
@bp.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    form = LoginForm()
    page = 'auth'
    
    if current_user.is_authenticated:
        return redirect(redirect_url('frontend.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print('------ {0}'.format(request.form))
            emailUsername = form.emailUsername.data
            pwd = form.pwd.data
            
            # get user from db with the email or username.
            personEmail = Person.query.filter(Person.email==emailUsername).first()
            personUsername = Person.query.filter(Person.username==emailUsername).first()
            
            # get next argument fro url
            next = request.args.get('next')
            if not next or url_parse(next).netloc != '':
                next = url_for('frontend.index')
            
            if personEmail:
                #check if the form password is same as hashed password and Log the user in
                verifyAndLogin(pwd, personEmail)
                sync_cart()
                response = make_response(redirect(next))
                response.set_cookie('cart_items', '', max_age=0, expires=0)
                return response
            elif personUsername:
                verifyAndLogin(pwd, personUsername)
                sync_cart()
                response = make_response(redirect(next))
                response.set_cookie('cart_items', '', max_age=0, expires=0)
                return response
            else:
                flash("Email/Username is incorrect or doesn't exist", 'error')
        else:
            print("\n\n", form.errors, "\n\n")
            flash("Something went Wrong. Please Try Again.", 'error')
    
    return render_template('frontend/auth/login.html', form=form, page=page)

## Route to Logout
@bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out", 'success')
    return redirect(redirect_url('frontend.login'))


