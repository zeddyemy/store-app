from datetime import date
from flask import current_app as app
from flask import request, url_for, flash, redirect, abort, jsonify
from flask_login import login_user
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy

from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.person import Person, Profile, Address
from app.models.role import Role

#-----------------------------------#
# Useful Functions
#-----------------------------------#
RESULTS_PER_PAGE = 5
def paginate_results(request, results):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    the_results = [result.format() for result in results]
    current_results = the_results[start:end]

    return current_results

def getCategoryNames():
    queryCategories = db.session.query(Category.name).order_by(desc('id')).all()
    print(queryCategories)
    CategoryNames = []
        
    for cat in queryCategories:
        CategoryNames.append(cat.name)
        
    return CategoryNames

def getAllCategories(cat_id='', pageNum=''):
    ''' Gets all Category rows from database
    
    This will return a pagination of all Category rows from database.
    :param cat_id: The ID of a Category. if cat_id is passed, it will return the sub categories of the category
    
    Alternatively, you can use getSubCategories(id) to get the sub categories without pagination
    '''
    
    if not pageNum:
        pageNum = request.args.get("page", 1, type=int)
    
    if not cat_id:
        allCategories = Category.query.order_by(desc('id'))
    elif cat_id:
        allCategories = Category.query.filter(Category.parent_id == cat_id).all()
        
    pagination = allCategories.paginate(pageNum, RESULTS_PER_PAGE)
    
    return pagination

def getSubCategories(parent_id):
    '''Gets all the sub categories of root Category'''
    subCategories = Category.query.filter(Category.parent_id == parent_id).all()
    return subCategories

def getProductsBYcategory(cat_id):
    '''Get all products belonging to a category as well as the child categories'''
    sub_query = db.session.query(Category.id).filter(Category.id == cat_id).union(
                db.session.query(Category.id).filter(Category.parent_id == cat_id)
            )
    return db.session.query(Product).join(Product.theCategory).filter(Product.category_id.in_(sub_query)).options(db.selectinload(Product.theCategory))

def getAllProducts(user_id='', cat_id='', pageNum='', json=False):
    ''' Gets all Products rows from database
    
    :param user_id: The ID of a User. If user_id is passed it will get
        ALL PRODUCTS that belong to the particular user
    :param cat_id: The ID of a Category. If cat_id is passed it will get
        ALL PRODUCTS from that particular Category
    IF BOTH are passed, it will get ALL PRODUCTS from that particular Category that belongs to the user
    
    :param pageNum: this should be request.args.get("page", 1, type=int)
        you can put it in a variable. Example shown below.
        
        EXAMPLE:
            pageNum = request.args.get("page", 1, type=int)
            
            allProducts = getAllProducts(user_id=1, cat_id=1, pageNum=pageNum)
    '''
    if not pageNum:
        pageNum = request.args.get("page", 1, type=int)
    
    if user_id and cat_id:
        allProducts = getProductsBYcategory(cat_id).filter_by(person_id=user_id)
    elif user_id:
        allProducts = Product.query.options(db.selectinload(Product.theCategory)).filter_by(person_id=user_id)
    elif cat_id:
        allProducts = getProductsBYcategory(cat_id)
    else:
        allProducts = Product.query.options(db.selectinload(Product.theCategory)).order_by(desc('id'))
    
    if json == True:
        pagination = allProducts.paginate(pageNum, RESULTS_PER_PAGE)
        formatPagination = [result.format() for result in pagination.items]
        
        #print('\n----allProducts----\n', allProducts, '\n--------------------\n')
        #print('\n----pagination----\n', pagination.items, '\n--------------------\n')
        #print('\n----iter_pages()----\n', pagination.iter_pages(), '\n--------------------\n')
        #print('\n----formatPagination----\n', formatPagination, '\n--------------------\n')
        
        if len(pagination.items) == 0:
            return jsonify({
                'success': False,
                'products': 0
            })
        elif len(pagination.items) > 0:
            return jsonify({
                'success': True,
                'total_products': len(pagination.items),
                'products': formatPagination,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next,
                'prev_num': pagination.prev_num,
                'next_num': pagination.next_num,
                'currentPage': pagination.page,
                'iter_pages': [page for page in pagination.iter_pages()],
            })
    
    #print('\n----allProducts----\n', allProducts, '\n--------------------\n')
    pagination = allProducts.paginate(pageNum, RESULTS_PER_PAGE)
    
    return pagination

def getRoleNames():
    'returns a list containing the names of all the roles'
    roleNames = []
    
    getAllRoles = db.session.query(Role.name).order_by(desc('id')).all()
    print(getAllRoles)
    for role in getAllRoles:
        roleNames.append(role.name)
        
            
    return roleNames

def getAllUsers(roleNames=None):
    '''
    Gets all Users rows from database.
    if no parameter is passed, it will get every user from the database
    if specific roles are passed as a parameter,
    it will get users that have the specified roles
    '''
    page = request.args.get("page", 1, type=int)
    getAllUser = Person.query.options(db.joinedload(Person.role), db.joinedload(Person.profile), db.joinedload(Person.address))
    
    if roleNames is not None:
        getAllUser = getAllUser.filter(Role.name.in_(roleNames))
    
    pagination = getAllUser.paginate(page, RESULTS_PER_PAGE)
    
    return pagination

def redirect_url(default='frontend.index'):
    return request.args.get('next') or request.referrer or \
        url_for(default)

def verifyAndLogin(password, theUser):
    '''
    This will Check if the provided 'password' is correct.
    If it's correct, it will log the user in.
    If the password isn't correct, it will flash a 'wrong password' message
    '''

    if theUser.verify_password(password):
        login_user(theUser)
        flash("Welcome back " + theUser.username, 'success')
    else:
        flash("Wrong Password - Please Try Again", 'error')

def urlParts():
    '''
    this splits the currents url into different parts
    and returns the different parts in form of an array
    '''
    url = request.base_url
    theUrlParts =url.split('/')
    
    return theUrlParts

def getUserInfo(userId):
    '''Gets profile details of a particular user'''
    
    if userId is None:
        userInfo = {}
    else:
        theUser = Person.query.filter(Person.id == userId).first()
        profile = Profile.query.filter(Profile.person_id == userId).first()
        address = Address.query.filter(Address.person_id == userId).first()
        
        userInfo = {
            'username': theUser.username,
            'email': theUser.email,
            'role': theUser.role.name,
            'firstname': profile.firstname,
            'lastname': profile.lastname,
            'phone': profile.phone,
            'profilePic': profile.profilePic,
            'city': address.city,
            'state': address.state,
            'country': address.country,
            'postalCode': address.postalCode,
            'defaultAddress': address.defaultAddress,
        }
    
    for key in userInfo:
        if userInfo[key] is None:
            userInfo[key] = ''
    
    return userInfo

def get_or_404(query):
    result = query.one_or_none()
    if result is None:
        abort(404)
    
    return result

def getRoleId(role):
    roleFromDb = Role.query.filter(Role.name == role).first()
    customerRole = Role.query.filter(Role.name == 'customer').first()
                    
    if roleFromDb:
        role_id = roleFromDb.id
    else:
        role_id = customerRole.id

    return role_id

def validateEmail(email, existingEmail):
    if email != existingEmail:
        user = Person.query.filter(Person.email == email).first()
        if user:
            flash('A user with this Email already registered! Please user another', 'error')
            return redirect(url_for('ctrlPanel.editUser'))
        else:
            return email
    else:
        return email

def validateUsername(username, existingUsername):
    if username != existingUsername:
        user = Person.query.filter(Person.username == username).first()
        if user:
            flash('A user with this Username already registered! Please user another', 'error')
            return redirect(url_for('ctrlPanel.editUser'))
        else:
            return username
    else:
        return username

def cpanelRoles():
    allRoles = Role.query.filter(Role.name != 'Customer').all()
    cpanelRoles = [role.name for role in allRoles]
    
    return cpanelRoles

def adminEditor_Roles():
    allRoles = Role.query.filter(Role.name.in_(['Administrator', 'Editor'])).all()
    adminEditorRoles = [role.name for role in allRoles]
    
    return adminEditorRoles
