from flask import Flask, Blueprint, render_template, redirect, url_for
from app.models import User, Product

main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

@main_bp.route('/about', methods=['GET'])
def about():
    return render_template('/main/about.html')

@main_bp.route('/fees', methods=['GET'])
def fees():
    return render_template('/main/fees.html')

@main_bp.route('/@<string:store_url>', methods=['GET'])
def user_store(store_url):
    query = User().custom_query('store_url', store_url).first()
    if not query:
        return redirect(url_for('main.four_o_four'))
    return render_template('/store/store.html', usr=query)

## Error handlers
@main_bp.route('/404', methods=['GET'])
def four_o_four():
    return render_template('/main/404.html')