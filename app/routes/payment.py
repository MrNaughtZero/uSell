from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, session, jsonify
from flask_login import current_user, login_required
from app.models import User, Product
from app.stripe_payments import account_setup, account_query, create_checkout

payment_bp = Blueprint("payment", __name__)

@payment_bp.route('/stripe/link', methods=['GET'])
@login_required
def link_stripe():
    setup = account_setup(User().custom_query('user_id', current_user.get_id()).first().email)
    session['acc_id'] = setup[0]

    return redirect(setup[1])

@payment_bp.route('/stripe/link/validate', methods=['GET'])
@login_required
def stripe_validate():
    if User().custom_query('user_id', current_user.get_id()).first().acc_id:
        return redirect(url_for('seller.dashboard'))
        
    if account_query(session['acc_id'])['charges_enabled']:
        return redirect(url_for('payment.stripe_success'))
    else:
        flash('Semething went wrong. Please try again later')
        return redirect(url_for('seller.dashboard'))

@payment_bp.route('/stripe/link/success', methods=['GET'])
@login_required
def stripe_success():
    User().update_stripe_status(session['acc_id'], current_user.get_id())
    session.pop('acc_id')

    flash('Stripe successfully linked')
    return redirect(url_for('seller.dashboard'))

@payment_bp.route('/checkout/', methods=['GET'])
def checkout():
    usr = User().custom_query('store_url', request.cookies.get('store_url')).first()

    for item in usr.product:
        price = int(item.item_price)*100
        name = item.item_name
        currency = item.item_currency
    
    session['checkoutId'] = create_checkout(usr.acc_id, price, name, currency, usr.user_id)
    
    return jsonify(session['checkoutId'])
