from app.database import db
from app.classes import Uploads
import hashlib
from hashlib import sha256
import string
from random import choice
from datetime import datetime
from flask_login import current_user

## Create new table to link up the tables; many to many

user_product = db.Table('user_product',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.product_id'))
)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    store_url = db.Column(db.String(200), nullable=True)
    activated = db.Column(db.Boolean, default=False, nullable=False)
    acc_id = db.Column(db.String(50), nullable=True)
    order = db.relationship('Order', backref='/order', lazy=True)
    
    def get_id(self):
        return self.user_id
    
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def create_user(self):
        self.password = self.hash_password(self.password)
        db.session.add(self)
        db.session.commit()
        return self

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value})

    def check_login(self, email, password):
        return self.query.filter_by(email=email, password=self.hash_password(password)).first()

    def update_store_name(self, user_id, store_url):
        self.query.filter_by(user_id=user_id).first().store_url = store_url
        db.session.commit()

    def update_stripe_status(self, acc_id, user_id):
        query = self.custom_query('user_id', user_id).first()
        query.activated = True
        query.acc_id = acc_id
        db.session.commit()

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def generate_state(length=50):
        generate = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(choice(generate) for i in range(length))

class Product(db.Model):
    __tablename__ = 'products'
    store_name = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_desc = db.Column(db.TEXT(500), nullable=False)
    item_currency = db.Column(db.String(50), nullable=False)
    item_price = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    product_link  = db.relationship('User', backref="product", secondary=user_product)

    def create_product(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        query = self.custom_query('product_id', self.product_id).first()
        
        for att in ('store_name', 'item_name', 'item_desc', 'item_currency', 'item_price', 'contact_email'):
            setattr(query, att, getattr(self, att))
        
        if "<FileStorage: ''" not in str(self.image):
            Uploads.remove_upload(query.image)
            query.image = Uploads(self.image).save_upload()

        db.session.commit()

    def custom_query(self, query, value):
        return self.query.filter_by(**{query:value})

    @staticmethod
    def appendTable(user, product):
        user.product.append(product)
        db.session.commit()

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.String(50), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    currency = db.Column(db.String(10), nullable=False)
    price_paid = db.Column(db.Float(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(50), default=str(datetime.now())[:-7])
    checkout_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Paid', nullable=False)
    shipping = db.relationship('Shipping', backref='/shipping', lazy=True)


    def as_dict(self):
        ''' return as dict // this is needed for when I do a fetch request with json '''
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def create_order(self):
        db.session.add(self)
        db.session.commit()

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value})

    def update_status(self, order_id):
        result = self.custom_query('order_id', order_id).first()
        if not result:
            return False
        result.status = 'Fulfilled'
        db.session.commit()
        return True

    @staticmethod
    def generate_order(length=6):
        ''' generate order ID until an ID is generated that doesn't already exist'''
        generate = string.ascii_uppercase + string.ascii_uppercase + string.digits
        returned_id = ''.join(choice(generate) for i in range(length))
        
        while(Order().custom_query('order_id', returned_id).first()):
            generate = string.ascii_uppercase + string.ascii_uppercase + string.digits
        return returned_id

class Shipping(db.Model):
    __tablename__ = 'shipping'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    line_one = db.Column(db.String(255), nullable=False)
    line_two = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=False)
    post_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    order_id = db.Column(db.String(50), db.ForeignKey('orders.order_id'))

    def add_shipping(self):
        db.session.add(self)
        db.session.commit()