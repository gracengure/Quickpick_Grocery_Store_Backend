#!/usr/bin/env python3
from models import db, User, Product, Order, OrderProduct
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import os
from datetime import date
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'grocery_store.db')}"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.config["JWT_SECRET_KEY"] = "super-secret"

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)
api = Api(app)
CORS(app)


@app.route("/")
def index():
    return "<h1>Quick pick groceries</h1>"


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        response = make_response(jsonify(error="Email already exists"), 422)
        return response

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=data.get("role", "customer"),
    )
    db.session.add(new_user)
    db.session.commit()
    response = make_response(jsonify(new_user_id=new_user.id), 201)
    return response


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    if user.email != data["email"]:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            response = make_response(jsonify(error="Email already exists"), 422)
            return response

    user.name = data["name"]
    user.email = data["email"]
    if "password" in data:
        user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user.role = data.get("role", user.role)
    db.session.commit()
    response = make_response(jsonify(message="User updated successfully"), 200)
    return response


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    response = make_response(
        jsonify(
            {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        ),
        200,
    )
    return response


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    response = make_response("", 204)
    return response


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        price=data["price"],
        category=data["category"],
        stock_quantity=data["stock_quantity"],
    )
    db.session.add(new_product)
    db.session.commit()
    response = make_response(jsonify(new_product_id=new_product.id), 201)
    return response


@app.route("/products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        response = make_response(
            jsonify([product.to_dict() for product in products]), 200
        )
        return response
    except Exception as e:
        response = make_response(jsonify({"error": "Internal Server Error"}), 500)
        return response

@app.route('/products/<category>', methods=['GET'])
def get_products_by_category(category):
    try:
        products = Product.query.filter(Product.category.ilike(category)).all()
        print(f"Found products: {products}")  # Debug statement
        if not products:
            return jsonify({"error": "No products found for this category"}), 404
        product_data = []
        for product in products:
            product_dict = product.to_dict()
            product_data.append(product_dict)
        return jsonify(product_data), 200
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    response = make_response(jsonify({
        'product_id': product.id,
        'name': product.name,
        'price': product.price,
        'category': product.category,
        'stock_quantity': product.stock_quantity,
        
    }), 200)
    response = make_response(
        jsonify(
            {
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "category": product.category,
                "stock_quantity": product.stock_quantity,
            }
        ),
        200,
    )
    return response


@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    product.name = data['name']
    product.price = data['price']
    product.category = data['category']
    product.stock_quantity = data['stock_quantity']
   
    
    db.session.commit()
    response = make_response(jsonify(message="Product updated successfully"), 200)
    return response


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    response = make_response("", 204)
    return response


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data["user_id"],
        order_date=date.today(),
        total_price=data["total_price"],
    )
    db.session.add(new_order)
    db.session.commit()
    response = make_response(jsonify(new_order_id=new_order.id), 201)
    return response


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    response = make_response(
        jsonify(
            {
                "order_id": order.id,
                "user_id": order.user_id,
                "order_date": order.order_date.isoformat(),
                "total_price": order.total_price,
            }
        ),
        200,
    )
    return response


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.user_id = data["user_id"]
    order.order_date = data["order_date"]
    order.total_price = data["total_price"]
    db.session.commit()
    response = make_response(jsonify(message="Order updated successfully"), 200)
    return response


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    response = make_response("", 204)
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5555)
