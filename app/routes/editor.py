from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.forms import RegisterForm, ProductForm
from app.models import Product, User
from app.classes import Uploads
from app.routes.auth import register_user

editor_bp = Blueprint("editor", __name__)

@editor_bp.route('/editor/edit', methods=['GET'])
def edit():
    if current_user.is_authenticated:
        return redirect(url_for('seller.dashboard'))
    return render_template('editor/edit.html', form=ProductForm(), register=RegisterForm())

@editor_bp.route('/editor/create', methods=['POST'])
def create():
    product = ProductForm()
    register = RegisterForm()
    
    if not (register.validate_on_submit()) or not (product.validate_on_submit()):
        return redirect(url_for('editor.edit'))

    reg_user = register_user(register.data.get('email'), register.data.get('password'))
    
    if not reg_user:
        return redirect(url_for('editor.edit'))
    
    if str(product.data.get('item_price')).endswith('.0') or str(product.data.get('item_price')):
        item_price = int(product.data.get('item_price'))
    else:
        item_price = product.data.get('item_price')

    add_product = Product(store_name=request.form.get('store_name'),
    item_name=product.data.get('item_name'),
    item_desc=product.data.get('item_desc'),
    item_currency=product.data.get('item_currency'),
    item_price=item_price,
    image=Uploads(request.files['item_img']).save_upload(),
    contact_email=product.data.get('contact_email')).create_product()
    
    if not add_product:
        return redirect(url_for('editor.edit'))

    Product.appendTable(reg_user, add_product)

    return redirect(url_for('seller.dashboard'))

@editor_bp.route('/editor/update/<id>', methods=['POST'])
@login_required
def update(id):
    usr = User().custom_query('user_id', current_user.get_id()).first()
    
    for item in usr.product:
        if str(id) != str(item.product_id):
            return redirect(url_for('main.four_o_four'))
    
    Product(product_id=id,
    store_name=request.form.get('store_name'),
    item_name=request.form.get('item_name'),
    item_desc=request.form.get('item_desc'),
    item_currency=request.form.get('item_currency'),
    item_price=request.form.get('item_price'),
    image=request.files['item_img'],
    contact_email=request.form.get('contact_email')).update()

    return redirect(url_for('seller.dashboard'))