from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
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
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError("Failed simple email validation")
        return value

    def __repr__(self):
        return f'<User id={self.id} name={self.name} email={self.email} role={self.role}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

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
    order_products = db.relationship('OrderProduct', back_populates='product')

    # Adding serialization rules
    serialize_rules = ('-order_products.product',)

    def __repr__(self):
        return f'<Product id={self.id} name={self.name} category={self.category} price={self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url
        }

# Order model
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)

    # Adding relationships
    order_products = db.relationship('OrderProduct', back_populates='order')
    user = db.relationship('User', back_populates='orders')

    # Adding serialization rules
    serialize_rules = ('-order_products.order', '-user.orders')

    def __repr__(self):
        return f'<Order id={self.id} user_id={self.user_id} order_date={self.order_date} total_price={self.total_price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_date': self.order_date,
            'total_price': self.total_price,
            'order_products': [op.to_dict() for op in self.order_products]
        }

# Association table for Order-Product Many-to-Many relationship
class OrderProduct(db.Model, SerializerMixin):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Adding relationships
    product = relationship('Product', back_populates='order_products')
    order = relationship('Order', back_populates='order_products')

    # Adding serialization rules
    serialize_rules = ('-product.order_products', '-order.order_products')

    def __repr__(self):
        return f'<OrderProduct order_id={self.order_id} product_id={self.product_id} quantity={self.quantity}>'

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'product': self.product.to_dict(),  # Include product details for convenience
        }
