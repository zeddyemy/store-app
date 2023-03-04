import sys
import os
import uuid as uuid
from werkzeug.utils import secure_filename
from slugify import slugify
from flask import render_template, request, Response, flash, redirect, abort, url_for
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from flask_login import login_required

from app.ctrl_panel import bp
from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.person import Person, Profile, Address
from app.models.role import Role
from app.forms import *
from app.help_functions.process_img import saveImage
from app.appfunctions import getAllCategories, redirect_url, get_or_404
from app.decorators import roles_required


@bp.route("/categories", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def categories():
    pageName = "categories"
    allCategories = getAllCategories()
    
    return render_template('cpanel/webpages/categories/categories.html', pageName=pageName, allCategories=allCategories)

## Route to add new category
@bp.route("/categories/new", methods=['GET', 'POST'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def addNew_category():
    error = False
    pageName = "categories"
    form = CategoryForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # get form data
            name = form.name.data
            description = form.description.data
            parent_cat = form.parent_cat.data
            cat_img = form.cat_img.data
            slug = slugify(name)
            
            try:
                # TODO: add functionality to check if category already exist in DB
                
                # Save the image file and return the id of the image in db
                if cat_img:
                    cat_img = saveImage(cat_img)
                if not cat_img:
                    cat_img = ""
                
                # get category from db where the name is same as parent_cat
                categoryFromDb = Category.query.filter(Category.name == parent_cat).first()
                if categoryFromDb:
                    parent_id = categoryFromDb.id
                else:
                    parent_id = None
                
                newCategory = Category(name=name, description=description, cat_img=cat_img, parent_id=parent_id, slug=slug)
                db.session.add(newCategory)
                db.session.commit()
            except Exception as e:
                error = True
                error_msg = f"An error occurred. {name} could not be created. \n Error: {e}"
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            if error:
                flash(error_msg, "error")
                print(description + ', ' + name + ', ')
                abort(500)
            else:
                # on successful db insert, flash success
                flash(f"{name} was successfully created!", "success")
        else:
            print("\n\n", form.errors, "\n\n")
            flash("New category was not created successfully.", 'error')

    return render_template('cpanel/webpages/categories/new_category.html', form=form, pageName=pageName)


## Route to edit category
@bp.route("/categories/edit/<slug>", methods=['GET', 'POST'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def edit_category(slug):
    error = False
    pageName = "categories"
    form = CategoryForm()
    
    category = Category.query.filter(Category.slug == slug).first()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if db.session.is_active:
                db.session.commit()
            db.session.begin()
            try:
                name = form.name.data
                description = form.description.data
                parent_cat = form.parent_cat.data
                cat_img = form.cat_img.data
                
                if cat_img:
                    cat_img = saveImage(cat_img) # This saves image file and return the fullpath to the image
                if not cat_img:
                    if category.cat_img:
                        cat_img = category.cat_img
                    else:
                        cat_img = ""
                
                # check if selected  parent category exist
                parentCat = Category.query.filter(Category.name == parent_cat).first()
                if parentCat:
                    parent_id = parentCat.id
                else:
                    parent_id = None
                
                category.name= name
                category.description= description
                category.cat_img= cat_img
                category.parent_id= parent_id
                
                db.session.commit()
            except Exception as e:
                error = True
                errMsg = f"An error occurred. {slug} could not be updated \n. Error: {e}"
                db.session.rollback()
                print(sys.exc_info())
                raise
            finally:
                db.session.close()
            if error:
                # on unsuccessful db insert, flash an error instead.
                # flash('An error occurred. we could not sign you Up. Please Try Again!', 'error')
                flash(f'{errMsg} - Please Try Again!', "error")
                abort(500)
            else:
                # on successful db insert, flash success
                flash('Category was successfully updated', 'success')
                return redirect(url_for('ctrlPanel.categories'))
        else:
            allFields = ['name', 'description']
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
    
    return render_template('cpanel/webpages/categories/edit_category.html', form=form, pageName=pageName, category=category)

## Route to delete category
@bp.route("/categories/delete/<slug>", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def del_category(slug):
    error = False
    
    try:
        uncategorized = Category.query.filter(Category.name == 'uncategorized').first()
        if not uncategorized:
            uncategorized = Category(name='uncategorized', slug='uncategorized')
            uncategorized.insert()
        
        # category to be deleted
        oldCategory = get_or_404(Category.query.filter(Category.slug == slug))
        
        # reassign all products in oldCategory to uncategorized
        for product in oldCategory.products:
            product.category_id = uncategorized.id
        
        db.session.commit()
        oldCategory.delete()
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
        flash('The category was successfully Deleted', 'success')
    
    return redirect(url_for('ctrlPanel.categories'))