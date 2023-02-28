import sys
import uuid as uuid
from flask import render_template, request, Response, flash, redirect, abort, url_for
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from flask_login import login_required, current_user

from app.ctrl_panel import bp
from app.extensions import db
from app.models.person import Person, Profile, Address
from app.forms import *
from app.help_functions.process_img import saveImage
from app.appfunctions import getAllCategories, getAllProducts, getAllUsers, redirect_url, getUserInfo
from app.decorators import roles_required


## Route for the admin Control Panel
@bp.route("/", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def index():
    pageName = "cpanel"
    allProducts = getAllProducts()
    
    allCategories = getAllCategories()
    
    return render_template('cpanel/webpages/home/index.html', pageName=pageName, totalProducts=0, totalCategories=0)


## Route to see profile
@bp.route("/profile", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def profilePage():
    pageName = "profile"
    userId = current_user.id
    
    
    userInfo = getUserInfo(userId)
    print("---------->>\n", userInfo, "\n<<----------\n")
    
    return render_template('cpanel/webpages/profile/index.html', pageName=pageName, userId=userId, userInfo=userInfo)

## Route to see profile
@bp.route("/profile/edit", methods=['GET', 'POST'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def editProfile():
    error = False
    pageName = "edit profile"
    form = editProfileForm()
    userId = current_user.id
    userInfo = getUserInfo(userId)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if db.session.is_active:
                db.session.commit()
            db.session.begin()
            try:
                firstname = form.firstname.data
                lastname = form.lastname.data
                username = form.username.data
                email = form.email.data
                phone = form.phone.data
                country = form.country.data
                state = form.state.data
                city = form.city.data
                postalCode = form.postalCode.data
                defaultAddress = form.defaultAddress.data
                otherAddresses = ''
                profilePic = form.profilePic.data
                
                if profilePic:
                    profilePic = saveImage(profilePic) # This saves image file and return the fullpath to the image
                if not profilePic:
                    if current_user.profile.profilePic:
                        profilePic = current_user.profile.profilePic
                    else:
                        profilePic = ""
                
                theUser = Person.query.filter(Person.id == userId).first()
                theUser.username = username
                theUser.email = email
                
                userProfile = theUser.profile
                userProfile.firstname = firstname
                userProfile.lastname = lastname
                userProfile.phone = phone
                userProfile.profilePic = profilePic
                
                userAddress = theUser.address
                userAddress.country = country
                userAddress.state = state
                userAddress.city = city
                userAddress.postalCode = postalCode
                userAddress.defaultAddress = defaultAddress
                
                db.session.commit()
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
                # flash('An error occurred. we could not sign you Up. Please Try Again!', 'error')
                flash(f'{errMsg} - Please Try Again!', "error")
                print("\n\n there was an error ", username )
                abort(500)
            else:
                # on successful db insert, flash success
                flash('You profile was successfully updated', 'success')
                return redirect(url_for('ctrlPanel.profilePage'))
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
    
    return render_template('cpanel/webpages/profile/edit_profile.html', pageName=pageName, form=form, userId=userId, userInfo=userInfo)

