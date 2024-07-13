#!/usr/bin/env python3

from app import app
from models import db, User, Product, Order, OrderProduct
from datetime import date

with app.app_context():

    print("Deleting data...")
    OrderProduct.query.delete()
    Order.query.delete()
    Product.query.delete()
    User.query.delete()

    print("Creating users...")
    user1 = User(name="John Doe", email="john@example.com", password="password", role="customer")
    user2 = User(name="Jane Smith", email="jane@example.com", password="password", role="customer")
    admin = User(name="Admin User", email="admin@example.com", password="password", role="admin")
    users = [user1, user2, admin]

    print("Creating products...")
    fruits = [
        Product(name="Apple", price=0.50, category="Fruits", stock_quantity=100, image_url="https://i.pinimg.com/564x/70/b5/92/70b592c1c8f78681dc5bd83bd2d660cf.jpg"),
        Product(name="Banana", price=0.30, category="Fruits", stock_quantity=150, image_url="https://i.pinimg.com/736x/67/ff/04/67ff0431ed4ecbf10ebed90c15eb6d0a.jpg"),
        Product(name="Orange", price=0.40, category="Fruits", stock_quantity=120, image_url="https://i.pinimg.com/564x/7a/aa/a5/7aaaa545e00e8a434850e80b8910dd94.jpg"),
        Product(name="Grapes", price=1.20, category="Fruits", stock_quantity=90, image_url="https://i.pinimg.com/564x/5d/ef/da/5defda60b0de8f3d67f0b362b38113e8.jpg"),
        Product(name="Strawberry", price=1.50, category="Fruits", stock_quantity=80, image_url="https://i.pinimg.com/564x/77/37/cc/7737cc5acaef557fea76441c3a484890.jpg"),
        Product(name="Pineapple", price=2.00, category="Fruits", stock_quantity=60, image_url="https://i.pinimg.com/564x/b5/fa/da/b5fada95c76dc2ba9aa6b40a008f7126.jpg"),
        Product(name="Mango", price=1.75, category="Fruits", stock_quantity=70, image_url="https://i.pinimg.com/564x/68/e4/73/68e473002d030395640718bc5462eabb.jpg"),
        Product(name="Blueberry", price=3.00, category="Fruits", stock_quantity=50, image_url="https://i.pinimg.com/564x/f3/09/2a/f3092ad2a730bdb5ac5bbb5631ada06e.jpg")
    ]

    grains = [
        Product(name="Rice", price=0.60, category="Grains", stock_quantity=200, image_url="https://i.pinimg.com/564x/aa/17/ff/aa17ff303c9e66cf42512319dab79248.jpg"),
        Product(name="Wheat", price=0.70, category="Grains", stock_quantity=180, image_url="https://i.pinimg.com/564x/cd/13/b9/cd13b98dfb9527f0d85b206fbbaebe28.jpg"),
        Product(name="Oats", price=1.10, category="Grains", stock_quantity=150, image_url="https://i.pinimg.com/564x/49/a0/21/49a021b279e14539d69c9c2dfa19035b.jpg"),
        Product(name="Barley", price=1.20, category="Grains", stock_quantity=130, image_url="https://i.pinimg.com/564x/0b/83/8d/0b838d8e0bde5a8e949ec17649142499.jpg"),
        Product(name="Quinoa", price=2.50, category="Grains", stock_quantity=100, image_url="https://i.pinimg.com/564x/ad/bd/87/adbd87796b9fa15bd7d8dfa4c83c7385.jpg"),
        Product(name="Corn", price=0.80, category="Grains", stock_quantity=170, image_url="https://i.pinimg.com/564x/c9/28/83/c92883a1c96a404ae49afc471e083f80.jpg"),
        Product(name="Millet(Ragi)", price=1.00, category="Grains", stock_quantity=160, image_url="https://i.pinimg.com/564x/49/ac/c4/49acc4f709c9859dff7a7b7b0c054285.jpg"),
        Product(name="Sorghum", price=1.30, category="Grains", stock_quantity=140, image_url="https://i.pinimg.com/564x/3a/f5/ed/3af5edcd35c2f0d06e03e8e68bf30310.jpg")
    ]

    vegetables = [
        Product(name="Carrot", price=0.40, category="Vegetables", stock_quantity=200, image_url="https://i.pinimg.com/564x/ba/05/18/ba05185d357cd59a97110b9a8a57fc31.jpg"),
        Product(name="Broccoli", price=0.90, category="Vegetables", stock_quantity=150, image_url="https://i.pinimg.com/564x/29/b3/cb/29b3cbe08421127f03eb643250590c00.jpg"),
        Product(name="Spinach", price=1.00, category="Vegetables", stock_quantity=180, image_url="https://i.pinimg.com/564x/28/28/d4/2828d4a7304777d3b25cf982574f7c2e.jpg"),
        Product(name="Potato", price=0.50, category="Vegetables", stock_quantity=300, image_url="https://i.pinimg.com/564x/86/92/1a/86921a331d7e84e48e009ffa2365a8bc.jpg"),
        Product(name="Tomato", price=0.70, category="Vegetables", stock_quantity=250, image_url="https://i.pinimg.com/564x/7a/82/04/7a82040e4c6033679ea5ee4789d80961.jpg"),
        Product(name="Purple onion", price=0.60, category="Vegetables", stock_quantity=220, image_url="https://i.pinimg.com/564x/94/e9/d8/94e9d8d1257eab907167f07da22f527f.jpg"),
        Product(name="Bell pepper", price=1.20, category="Vegetables", stock_quantity=140, image_url="https://i.pinimg.com/564x/7a/13/14/7a13144182a6dc831a37247134400fd3.jpg"),
        Product(name="Lettuce", price=0.80, category="Vegetables", stock_quantity=160, image_url="https://i.pinimg.com/564x/90/0c/55/900c55aecb673eb2e025b67f41e09b8a.jpg")
    ]

    products = fruits + grains + vegetables

    print("Creating orders...")
    order1 = Order(user=user1, order_date=date(2024, 3, 3), total_price=10.0)
    order2 = Order(user=user2, order_date=date(2024, 4, 5), total_price=15.0)
    orders = [order1, order2]

    print("Creating order_products...")
    op1 = OrderProduct(order=order1, product=fruits[0], quantity=10)  # Apple
    op2 = OrderProduct(order=order1, product=grains[0], quantity=5)   # Rice
    op3 = OrderProduct(order=order2, product=vegetables[0], quantity=8)  # Carrot
    op4 = OrderProduct(order=order2, product=fruits[2], quantity=3)   # Orange
    op5 = OrderProduct(order=order2, product=vegetables[3], quantity=6)  # Potato
    order_products = [op1, op2, op3, op4, op5]

    db.session.add_all(users)
    db.session.add_all(products)
    db.session.add_all(orders)
    db.session.add_all(order_products)
    db.session.commit()

    print("Seeding done!")