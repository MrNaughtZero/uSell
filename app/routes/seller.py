from flask import Flask, Blueprint, render_template, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, current_user
from app.forms import RegisterForm, ProductForm, StoreUrl
from app.models import Product, User, Order
## commit removed simplejson here

seller_bp = Blueprint("seller", __name__)

@seller_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    usr = User().custom_query('user_id', current_user.get_id()).first()
    
    return render_template('/seller/dashboard.html', form=ProductForm(), store=StoreUrl(), usr=usr, message=get_flashed_messages(), orders=Order().custom_query('user_id' , current_user.get_id()).all())

@seller_bp.route('/url/check/<string:store_url>', methods=['GET'])
@login_required
def check_url(store_url):
    if User().custom_query('store_url', store_url).first():
        return jsonify({'Success': True}), 400
    
    User().update_store_name(current_user.get_id(), store_url)
    return jsonify({'Success': True}), 200

@seller_bp.route('/show/order/<string:orderId>', methods=['GET'])
@login_required
def show_order(orderId):
    result = Order().custom_query('order_id', orderId).first()
    if not result:
        return jsonify({'Success': False}), 400

    
    output = {}
    for item in result.shipping:
        output.update(item.__dict__)

    output['email'] = result.email
    output['status'] = result.status
    output['order_id'] = result.order_id
    output.pop('_sa_instance_state')

    return jsonify(output)

@seller_bp.route('/show/order/<string:order_id>/update/status', methods=['GET'])
@login_required
def mark_order(order_id):
    if not Order().update_status(order_id):
        return jsonify({'Success': False}), 400

    return jsonify({'Success': True}), 200