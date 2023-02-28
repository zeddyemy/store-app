import sys
from werkzeug.urls import url_parse
from slugify import slugify
from flask import render_template, request, Response, flash, redirect, url_for, abort
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.ctrl_panel import bp
from app.extensions import db
from app.appfunctions import redirect_url, verifyAndLogin
from app.models.person import Person, Profile, Address
from app.models.role import Role
from app.forms import *
from app.decorators import roles_required


## Route to sign up user
@bp.route("/signup", methods=['GET', 'POST'])
def signUp():
    error = False
    form = SignUpForm()
    
    if current_user.is_authenticated:
        return redirect(redirect_url('ctrlPanel.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print('------ {0}'.format(request.form))
            try:
                username = form.username.data
                email = form.email.data
                firstname = form.firstname.data
                lastname = form.lastname.data
                slug = slugify(username)
                password = form.password.data
                
                hashedPw = generate_password_hash(password, "sha256")
                personRole = Role.query.filter(Role.name=='trader').first()
                if personRole:
                    personRoleId = personRole.id
                
                newPerson = Person(username=username, email=email, thePassword=hashedPw, role_id=personRoleId, slug=slug)
                newPersonProfile = Profile(firstname=firstname, lastname=lastname, person=newPerson)
                newPersonAddress = Address(defaultAddress='', person=newPerson)
            
                db.session.add_all([newPerson, newPersonProfile, newPersonAddress])
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
                print("\n----------------->\n There was an error: ", errMsg, "\n<---------------\n" )
                abort(500)
            else:
                # on successful db insert, flash success
                flash('You account have been successfully created', 'success')
                return redirect(redirect_url('ctrlPanel.login'))
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
                        
    return render_template('cpanel/auth/sign_up.html', form=form, page='auth')

## Route to Login
@bp.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    form = LoginForm()
    
    if current_user.is_authenticated:
        return redirect(redirect_url('ctrlPanel.index'))
    
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
                next = url_for('ctrlPanel.index')
            
            if personEmail:
                #check if the form password is same as hashed password and Log the user in
                verifyAndLogin(pwd, personEmail)
                return redirect(next)
            elif personUsername:
                verifyAndLogin(pwd, personUsername)
                return redirect(next)
            else:
                flash("Email/Username is incorrect or doesn't exist", 'error')
        else:
            print("\n\n", form.errors, "\n\n")
            flash("Something went Wrong. Please Try Again.", 'error')
    
    return render_template('cpanel/auth/login.html', form=form, page='auth')

## Route to Logout
@bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out", 'success')
    return redirect(url_for('ctrlPanel.login'))

## route to add the admin user
@bp.route("/administrator", methods=['GET'])
def admin():
    error = False
    try:
        allRoles = Role.query.all()
        if len(allRoles) < 1:
            # Create all roles for the store
            administrator = Role(name='administrator')
            editor = Role(name='editor')
            trader = Role(name='trader')
            customer = Role(name='customer')
            db.session.add_all([administrator, editor, trader, customer])
            # db.session.add(Role)
            db.session.commit()
    
        # Create 'AdminUser' with 'administrator' roles
        adminRole = Role.query.filter(Role.name=='administrator').first()
        adminRoleId = adminRole.id
        adminUser = Person.query.filter(Person.role_id==adminRoleId).first()
        
        print("\n-------->>\n", adminUser, "\n<<---------\n\n")
        
        if adminUser:
            flash('please login to access the Control Panel', 'info')
            return redirect(redirect_url('ctrlPanel.login'))
        if not adminUser:
            hashedPw = generate_password_hash('root', "sha256")
            theAdminUser = Person(username='admin', email='AdminUser@mail.com', thePassword=hashedPw, role_id=adminRoleId, slug = slugify('admin'))
            theAdminUserProfile = Profile(firstname='Admin', person=theAdminUser)
            theAdminUserAddress = Address(defaultAddress='', person=theAdminUser)
            
            db.session.add_all([theAdminUser, theAdminUserProfile, theAdminUserAddress])
            db.session.commit()
    except Exception as e:
        error = True
        errMsg = e
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # on unsuccessful db insert, flash an error instead.
        print("\n----------------->\n There was an error: ", errMsg, "\n<---------------\n" )
        abort(500)
    else:
        adminUser = Person.query.filter(Person.role_id==adminRoleId).first()
        login_user(adminUser)
        # on successful db insert, flash success
        flash('Welcome to your Dashboard. You can oversea everything on your site from here', 'success')
    
    return redirect(redirect_url('ctrlPanel.index'))

