import sys
import os
import uuid as uuid
from slugify import slugify
from flask import render_template, request, Response, flash, redirect, abort, url_for
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from flask_login import login_required, current_user

from app.ctrl_panel import bp
from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.role import Role
from app.forms import *
from app.help_functions.process_img import saveImage
from app.appfunctions import getAllProducts, redirect_url, get_or_404
from app.decorators import roles_required


@bp.route("/products", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def products():
    pageName = "products"
    pageNum = request.args.get("page", 1, type=int)
    currentUserRole = current_user.role.name
    currentUserId = current_user.id
    
    if currentUserRole == 'trader':
        allProducts = getAllProducts(user_id=currentUserId, pageNum=pageNum)
    else:
        allProducts = getAllProducts(pageNum=pageNum)
        
    print('\n', allProducts.items, '<------ allProds\n')
    
    return render_template('cpanel/webpages/products/products.html', pageName=pageName, allProducts=allProducts)

## Route to add new product
@bp.route("/products/new", methods=['GET', 'POST'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def addNew_product():
    error = False
    pageName = "products"
    form = ProductForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print('------ {0}'.format(request.form))
            try:
                # get form data
                name = form.name.data
                description = form.description.data
                sellingPrice = form.sellingPrice.data
                actualPrice = form.actualPrice.data
                sizes = ",".join(form.selectAvailableSizes.data)
                colors = form.colors.data
                productCat = form.productCat.data
                product_img = form.product_img.data
                slug = slugify(name)
                person_id = current_user.id
                
                if product_img:
                    product_img = saveImage(product_img) # This saves image file and return the fullpath to the image
                if not product_img:
                    product_img = ""
                
                # get category from db where the name is same as form productCat
                categoryFromDb = Category.query.filter(Category.name == productCat).first()
                if categoryFromDb:
                    category_id = categoryFromDb.id
                else:
                    category_id = None
                    
                newProduct = Product(
                    name=name, description=description, sellingPrice=sellingPrice,
                    actualPrice=actualPrice, sizes=sizes, colors=colors, product_img=product_img, 
                    category_id=category_id, slug=slug, person_id=person_id
                )
                db.session.add(newProduct)
                db.session.commit()
            except:
                error = True
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            if error:
                flash('An error occurred. Your Product ' + request.form['name'] + ' could not be published.', 'error')
                abort(500)
            else:
                # on successful db insert, flash success
                flash('Your New Product ' + request.form['name'] + ' was successfully published!', 'success')
        else:
            print("\n\n", form.errors, "\n\n")
            flash("Product was not published successfully. Please try again", 'error')
    
    return render_template('cpanel/webpages/products/new_product.html', form=form, pageName=pageName)

## Route to edit product
@bp.route("/products/edit/<slug>", methods=['GET', 'POST'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def edit_product(slug):
    error = False
    pageName = "products"
    form = ProductForm()
    
    product = Product.query.filter(Product.slug == slug).first()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            if db.session.is_active:
                db.session.commit()
            db.session.begin()
            try:
                # get form data
                name = form.name.data
                description = form.description.data
                sellingPrice = form.sellingPrice.data
                actualPrice = form.actualPrice.data
                sizes = ",".join(form.selectAvailableSizes.data)
                colors = form.colors.data
                productCat = form.productCat.data
                product_img = form.product_img.data
                slug = slugify(name)
                
                
                if product_img:
                    product_img = saveImage(product_img) # This saves image file and return the fullpath to the image
                if not product_img:
                    if product.product_img:
                        product_img = product.product_img
                    else:
                        product_img = ""
                
                # check if selected  product category exist
                categoryExist = Category.query.filter(Category.name == productCat).first()
                if categoryExist:
                    category_id = categoryExist.id
                else:
                    category_id = None
                
                product.name = name
                product.description = description
                product.sellingPrice = sellingPrice
                product.actualPrice = actualPrice
                product.sizes = sizes
                product.colors = colors
                product.category_id = category_id
                product.product_img = product_img
                
                product.update()
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
                print("\n\n there was an error >>>>", name )
                abort(500)
            else:
                # on successful db insert, flash success
                flash('Product was successfully updated', 'success')
                return redirect(url_for('ctrlPanel.products'))
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
    
    return render_template('cpanel/webpages/products/edit_product.html', form=form, pageName=pageName, product=product)


## Route to delete product
@bp.route("/products/delete/<slug>", methods=['GET'])
@login_required
@roles_required('administrator', 'editor', 'trader')
def del_product(slug):
    error = False
    pageName = "products"
    
    try:
        product = get_or_404(Product.query.filter(Product.slug == slug))
        product.delete()
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
        flash('Product was successfully Deleted', 'success')
    
    return redirect(url_for('ctrlPanel.products'))

