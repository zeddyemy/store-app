import sys
from flask import render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_login import login_user, current_user
from app.frontend import bp
from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.person import Person
from app.appfunctions import paginate_results, getAllCategories, getSubCategories, getCategoryNames, getAllProducts, get_or_404
from app.decorators import frontendLogin_required


# Home page
@bp.route('/')
def index():
    page = 'home'
    pageNum = request.args.get("page", 1, type=int)
    
    # get root categories from db (categories without parent_id)
    rootCategories = Category.query.filter(Category.parent_id == None).all()
    allProducts = getAllProducts(pageNum=pageNum)
    
    return render_template('frontend/webpages/index.html', rootCategories=rootCategories, allProducts=allProducts, page=page)

# Products page
@bp.route('/products')
def allProducts():
    page = 'products'
    pageNum = request.args.get("page", 1, type=int)
    allProducts = getAllProducts(pageNum=pageNum)
    
    
    return render_template('frontend/webpages/products/index.html', allProducts=allProducts, page=page)

# Page to show Products in a category. (The content of a category)
@bp.route("/category/<slug>")
def showCatProducts(slug):
    page = 'categoryProd'
    pageNum = request.args.get("page", 1, type=int)
    
    # fetch category by slug
    category = get_or_404(Category.query.filter(Category.slug == slug))
    if category.parent_id:
        allProducts = getAllProducts(cat_id=category.id, pageNum=pageNum)
        productCat = category.slug
        category = get_or_404(Category.query.filter(Category.id == category.parent_id))
        subCategories = getSubCategories(category.id)
        
        return render_template('frontend/webpages/category.html', category=category, subCategories=subCategories, allProducts=allProducts, productCat=productCat, page=page)
    
    productCat = category.slug
    subCategories = getSubCategories(category.id)
    allProducts = getAllProducts(cat_id=category.id, pageNum=pageNum)
    
    return render_template('frontend/webpages/category.html', category=category, subCategories=subCategories, allProducts=allProducts, productCat=productCat, page=page)

# get Products in a category in JSON Format
@bp.route("/products-json/<catId>")
def getProducts(catId):
    pageNum = request.args.get("page", 1, type=int)
    
    try:
        allProducts = getAllProducts(cat_id=catId, pageNum=pageNum, json=True)
        return allProducts
    except:
        abort(404)

# page to view product details
@bp.route("/product/<slug>")
def productDetails(slug):
    page = 'productInfo'
    
    # query product by slug
    product = get_or_404(Product.query.filter(Product.slug == slug))
    sizes = product.sizes
    if not sizes:
        productSizes = None
    else:
        productSizes = sizes.split(',')
    
    colors = product.colors
    productColors = colors.split(',')
    
    
    print("\n\n", sizes, " ----> SIZES")
    print("\n", productSizes, " ----> PRODUCT SIZES \n")
    print("\n", productColors, " ----> PRODUCT COLORS \n")
    
    return render_template('frontend/webpages/product.html', product=product, productSizes=productSizes, productColors=productColors, page=page)


# checkout page
@bp.route("/checkout")
def checkOut():
    page = 'checkout'
    return render_template('frontend/webpages/checkout.html', page=page)

