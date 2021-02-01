from flask import Flask, Blueprint, render_template, flash, redirect, get_flashed_messages, url_for, request, jsonify, json
from app.models import User
from app.forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/auth/login', methods=['GET'])
def login():
    return render_template('/auth/login.html', message=get_flashed_messages(), form=LoginForm())

@auth_bp.route('/auth/login/attempt', methods=['POST'])
def login_attempt():
    query = User().check_login(request.form.get('email'), request.form.get('password'))
    
    if not query:
        flash('Incorrect Login Details')
        return redirect(url_for('auth.login'))

    login_user(query)
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/auth/check/<string:email>', methods=['GET'])
def check_email(email):
    if User().custom_query('email', email).first():
        return redirect(url_for('main.four_o_four'), 404)
    return jsonify({'Success': True}), 200

def register_user(email, password):
    if current_user.is_authenticated:
        return redirect(url_for('seller.dashboard'))
    if User().custom_query('email', email).first():
        return False
    
    query = User(email=email, password=password).create_user()
    if not query:
        return redirect(url_for('editor.edit'))

    login_user(query)
    return query

@auth_bp.route('/auth/logout', methods=['GET'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    logout_user()
    return redirect(url_for('main.index'))