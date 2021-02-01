from flask import Flask, Blueprint, session, redirect, url_for
from os import environ, urandom

app = Flask(__name__)
app.debug = True
app.secret_key = urandom(24)

## Error handlers

def page_not_found(e):
    return redirect(url_for('main.four_o_four'))

def not_found(e):
    return redirect(url_for('main.four_o_four'))

app.register_error_handler(404, page_not_found)
app.register_error_handler(400, not_found)


from .routes import auth, main, editor, seller, payment, order
 
app.register_blueprint(auth.auth_bp)
app.register_blueprint(main.main_bp)
app.register_blueprint(editor.editor_bp)
app.register_blueprint(seller.seller_bp)
app.register_blueprint(payment.payment_bp)
app.register_blueprint(order.order_bp)

from app.database import setup_db

setup_db(app, environ.get('DATABASE_PATH'))

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)