from flask import Flask, Blueprint, render_template, redirect, url_for, session
from app.models import Order, User, Shipping
from app.stripe_payments import retrieve_order

order_bp = Blueprint("order", __name__)

@order_bp.route('/create/order', methods=['GET'])
def create_order():
    result = retrieve_order(session['checkoutId'])
    session['order_id'] = Order.generate_order()
    
    Order(order_id=session['order_id'],
    user_id=result['client_reference_id'],
    currency=result['currency'],
    price_paid=float(result['amount_total'])/100,
    email=result['customer_details']['email'],
    checkout_id=result['id']).create_order()
    
    Shipping(name=result['shipping']['name'],
    line_one=result['shipping']['address']['line1'],
    line_two=result['shipping']['address']['line2'],
    city=result['shipping']['address']['city'],
    post_code=result['shipping']['address']['postal_code'],
    country=result['shipping']['address']['country'],
    order_id=session['order_id']).add_shipping()
    
    session.pop('checkoutId')
    
    return redirect(url_for('order.order_confirmation', orderId=session['order_id']))

@order_bp.route('/order/confirmation/<string:orderId>', methods=['GET'])
def order_confirmation(orderId):
    order_information = Order().custom_query('order_id', orderId).first()
    if not order_information:
        return redirect(url_for('main.four_o_four'))

    return render_template('/store/order-confirmation.html', order=order_information, usr=User().custom_query('user_id', order_information.user_id).first())

@order_bp.route('/cancel/order/<int:user>', methods=['GET'])
def cancel_order(user):
    query = User().custom_query('user_id', user).first()
    if not query:
        return redirect(url_for('main.four_o_four'), 404)
    return redirect(url_for('main.user_store', store_url=query.store_url))