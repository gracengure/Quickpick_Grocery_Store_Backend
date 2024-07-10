from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Metadata with naming convention for foreign keys
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='customer')

    # Adding relationship
    orders = db.relationship('Order', back_populates='user')
    
    # Adding serialization rules
    serialize_rules = ('-orders.user',)

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Invalid email'
        return email

# Product model
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(150), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    # Adding relationship
    order_items = db.relationship('OrderItem', back_populates='product')
     
    # Adding serialization rules
    serialize_rules = ('-order_items.product',)

# Order model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)

    # Adding relationship
    order_items = db.relationship('OrderItem', back_populates='order')
    user = db.relationship('User', back_populates='orders')
    
    # Adding serialization rules
    serialize_rules = ('-order_items.order', '-user.orders')

# Association table for Order-Product Many-to-Many relationship
class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Adding relationship
    product = relationship('Product', back_populates='order_items')
    order = relationship('Order', back_populates='order_items')

    # Adding serialization rules
    serialize_rules = ('-product.order_items', '-order.order_items')
