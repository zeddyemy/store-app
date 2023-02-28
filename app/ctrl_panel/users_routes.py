import sys
from werkzeug.urls import url_parse
from slugify import slugify
from flask import render_template, request, Response, flash, redirect, url_for, abort
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from app.ctrl_panel import bp
from app.extensions import db
from app.appfunctions import getAllUsers, redirect_url, get_or_404, validateEmail, validateUsername, getRoleId
from app.decorators import roles_required
from app.models.person import Person, Profile, Address
from app.models.role import Role
from app.forms import *


## Route to see list of users
@bp.route("/users", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def users():
    pageName = "users"
    allUsers = getAllUsers(roleNames=["administrators", "editor", "trader"])
    
    return render_template('cpanel/webpages/users/users.html', pageName=pageName, allUsers=allUsers)

## Route for admin to add new user that can access the dashboard
@bp.route("/users/new", methods=['GET', 'POST'])
@login_required
@roles_required('administrator')
def addNew_User():
    page = "users"
    error = False
    form = adminUsersForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                username = form.username.data
                email = form.email.data
                firstname = form.firstname.data
                lastname = form.lastname.data
                password = form.password.data
                slug = slugify(username)
                role = form.role.data
                
                # get role from db where the name is same as form role
                personRole = Role.query.filter(Role.name == role).first()
                if personRole:
                    personRoleId = personRole.id
                
                hashedPw = generate_password_hash(password, "sha256")
                newPerson = Person(username=username, email=email, thePassword=hashedPw, role_id=personRoleId, slug=slug)
                newPersonProfile = Profile(firstname=firstname, lastname=lastname, person=newPerson)
                newPersonAddress = Address(person=newPerson)
            
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
                flash("New users has been successfully added. Login details will be sent to user's Email", 'success')
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
    
    return render_template('cpanel/webpages/users/new_user.html', form=form, page=page)

## Route for admin to edit user that can access the dashboard
@bp.route("/users/edit/<slug>", methods=['GET', 'POST'])
@login_required
@roles_required('administrator')
def editUser(slug):
    pageName = "users"
    error = False
    form = adminEditUserForm()
    
    user = Person.query.filter(Person.slug == slug).first()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if db.session.is_active:
                db.session.commit()
            db.session.begin()
            
            try:
                username = form.username.data
                existingUsername = form.existingUsername.data
                email = form.email.data
                existingEmail = form.existingEmail.data
                role = form.role.data
                
                role_id = getRoleId(role) # get role id
                username = validateUsername(username, existingUsername)
                email = validateEmail(email, existingEmail)
                
                user.username= username
                user.email= email
                user.role_id= role_id
                
                user.update()
            except InvalidRequestError:
                db.session.rollback()
                flash(f"Something went wrong!", "danger")
            except IntegrityError as m:
                db.session.rollback()
                print(sys.exc_info())
                flash(f"User already exists!.", "warning")
                print("\n----------------->\n There was an error: ", m, "\n<---------------\n" )
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
                raise
            finally:
                db.session.close()
            if error:
                # on unsuccessful db insert, flash an error instead.
                print("\n----------------->\n There was an error: ", errMsg, "\n<---------------\n" )
                abort(500)
            else:
                # on successful db insert, flash success
                flash('User was successfully Edited', 'success')
                return redirect(url_for('ctrlPanel.users'))
        else:
            allFields = ['email', 'username']
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
    
    return render_template('cpanel/webpages/users/edit_user.html', form=form, pageName=pageName, user=user)

## Route for admin to delete user that can access the dashboard
@bp.route("/users/delete/<slug>", methods=['GET'])
@login_required
@roles_required('administrator')
def del_user(slug):
    error = False
    pageName = "users"
    
    try:
        user = get_or_404(Person.query.filter(Person.slug == slug))
        user.delete()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        raise
    finally:
        db.session.close()
    if error:
        # on unsuccessful db insert, flash an error instead.
        # flash('An error occurred. we could not sign you Up. Please Try Again!', 'error')
        flash(f'something went wrong - Please Try Again!', "error")
        print("\n\n there was an error >>>>" )
        abort(422)
    else:
        # on successful db insert, flash success
        flash('User was successfully Deleted', 'success')
    
    return redirect(url_for('ctrlPanel.users'))
    