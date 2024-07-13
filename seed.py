# Corrected seed.py
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
    user1 = User(name="John Doe", email="john@example.com", password="password", role="customer", phone_number="1234567890")
    user2 = User(name="Jane Smith", email="jane@example.com", password="password", role="customer", phone_number="0987654321")
    admin = User(name="Admin User", email="admin@example.com", password="password", role="admin", phone_number="1122334455")
    users = [user1, user2, admin]

    print("Creating products...")
    fruits = [
        Product(name="Apple", price=0.50, category="Fruits", stock_quantity=100, image_url="https://i.pinimg.com/564x/70/b5/92/70b592c1c8f78681dc5bd83bd2d660cf.jpg", description="Fresh apples", supplier="Orchard Fresh"),
        Product(name="Banana", price=0.30, category="Fruits", stock_quantity=150, image_url="https://i.pinimg.com/736x/67/ff/04/67ff0431ed4ecbf10ebed90c15eb6d0a.jpg", description="Ripe bananas", supplier="Tropical Harvest"),
        Product(name="Orange", price=0.40, category="Fruits", stock_quantity=120, image_url="https://i.pinimg.com/564x/7a/aa/a5/7aaaa545e00e8a434850e80b8910dd94.jpg", description="Juicy oranges", supplier="Citrus Grove"),
        Product(name="Grapes", price=1.20, category="Fruits", stock_quantity=90, image_url="https://i.pinimg.com/564x/5d/ef/da/5defda60b0de8f3d67f0b362b38113e8.jpg", description="Seedless grapes", supplier="Vineyard Co."),
        Product(name="Strawberry", price=1.50, category="Fruits", stock_quantity=80, image_url="https://i.pinimg.com/564x/77/37/cc/7737cc5acaef557fea76441c3a484890.jpg", description="Sweet strawberries", supplier="Berry Fields"),
        Product(name="Pineapple", price=2.00, category="Fruits", stock_quantity=60, image_url="https://i.pinimg.com/564x/b5/fa/da/b5fada95c76dc2ba9aa6b40a008f7126.jpg", description="Fresh pineapple", supplier="Tropical Harvest"),
        Product(name="Mango", price=1.75, category="Fruits", stock_quantity=70, image_url="https://i.pinimg.com/564x/68/e4/73/68e473002d030395640718bc5462eabb.jpg", description="Tropical mangoes", supplier="Tropical Harvest"),
        Product(name="Blueberry", price=3.00, category="Fruits", stock_quantity=50, image_url="https://i.pinimg.com/564x/f3/09/2a/f3092ad2a730bdb5ac5bbb5631ada06e.jpg", description="Organic blueberries", supplier="Berry Fields")
    ]

    grains = [
        Product(name="Rice", price=0.60, category="Grains", stock_quantity=200, image_url="https://i.pinimg.com/564x/aa/17/ff/aa17ff303c9e66cf42512319dab79248.jpg", description="Long grain rice", supplier="Grain Co."),
        Product(name="Wheat", price=0.70, category="Grains", stock_quantity=180, image_url="https://i.pinimg.com/564x/cd/13/b9/cd13b98dfb9527f0d85b206fbbaebe28.jpg", description="Whole wheat", supplier="Grain Co."),
        Product(name="Oats", price=1.10, category="Grains", stock_quantity=150, image_url="https://i.pinimg.com/564x/49/a0/21/49a021b279e14539d69c9c2dfa19035b.jpg", description="Rolled oats", supplier="Grain Co."),
        Product(name="Barley", price=1.20, category="Grains", stock_quantity=130, image_url="https://i.pinimg.com/564x/0b/83/8d/0b838d8e0bde5a8e949ec17649142499.jpg", description="Hulled barley", supplier="Grain Co."),
        Product(name="Quinoa", price=2.50, category="Grains", stock_quantity=100, image_url="https://i.pinimg.com/564x/ad/bd/87/adbd87796b9fa15bd7d8dfa4c83c7385.jpg", description="Organic quinoa", supplier="Superfood Supplies"),
        Product(name="Corn", price=0.80, category="Grains", stock_quantity=170, image_url="https://i.pinimg.com/564x/c9/28/83/c92883a1c96a404ae49afc471e083f80.jpg", description="Sweet corn", supplier="Grain Co."),
        Product(name="Millet", price=1.00, category="Grains", stock_quantity=160, image_url="https://i.pinimg.com/564x/49/ac/c4/49acc4f709c9859dff7a7b7b0c054285.jpg", description="Ragi Finger millet", supplier="Grain Co."),
        Product(name="Sorghum", price=1.30, category="Grains", stock_quantity=140, image_url="https://i.pinimg.com/564x/3a/f5/ed/3af5edcd35c2f0d06e03e8e68bf30310.jpg", description="Whole sorghum", supplier="Grain Co.")
    ]

    vegetables = [
        Product(name="Carrot", price=0.40, category="Vegetables", stock_quantity=200, image_url="https://i.pinimg.com/564x/ba/05/18/ba05185d357cd59a97110b9a8a57fc31.jpg", description="Fresh carrots", supplier="Vegetable Farm"),
        Product(name="Broccoli", price=0.90, category="Vegetables", stock_quantity=150, image_url="https://i.pinimg.com/564x/29/b3/cb/29b3cbe08421127f03eb643250590c00.jpg", description="Organic broccoli", supplier="Green Leaf Produce"),
        Product(name="Spinach", price=1.00, category="Vegetables", stock_quantity=180, image_url="https://i.pinimg.com/564x/28/28/d4/2828d4a7304777d3b25cf982574f7c2e.jpg", description="Fresh spinach", supplier="Green Leaf Produce"),
        Product(name="Potato", price=0.50, category="Vegetables", stock_quantity=300, image_url="https://i.pinimg.com/564x/d1/4b/49/d14b49a4c1125b376b4878d52f0a583e.jpg", description="Versatile potatoes", supplier="Vegetable Farm"),
        Product(name="Tomato", price=0.70, category="Vegetables", stock_quantity=220, image_url="https://i.pinimg.com/564x/79/7e/96/797e9652123593bd04cc0b1970403132.jpg", description="Juicy tomatoes", supplier="Vegetable Farm"),
        Product(name="Cucumber", price=0.60, category="Vegetables", stock_quantity=170, image_url="https://i.pinimg.com/564x/5b/22/65/5b2265dacf4826d6f826bcb9691f8d19.jpg", description="Crisp cucumbers", supplier="Vegetable Farm"),
        Product(name="Bell Pepper", price=0.80, category="Vegetables", stock_quantity=160, image_url="https://i.pinimg.com/564x/bd/15/f5/bd15f5863856d1c12cf840f788fd7af4.jpg", description="Sweet bell peppers", supplier="Green Leaf Produce"),
        Product(name="Onion", price=0.30, category="Vegetables", stock_quantity=250, image_url="https://i.pinimg.com/564x/e3/57/97/e357979e008e839aa6eafadf95ff2feb.jpg", description="Basic cooking onions", supplier="Vegetable Farm")
    ]

    orders = [
        Order(user=user1, order_date=date.today(), total_price=30.00),  # Corrected parameter
        Order(user=user2, order_date=date.today(), total_price=50.00),  # Corrected parameter
        Order(user=user1, order_date=date.today(), total_price=25.00),  # Corrected parameter
        Order(user=user2, order_date=date.today(), total_price=40.00)   # Corrected parameter
    ]

    print("Adding data to the database...")
    db.session.add_all(users)
    db.session.add_all(fruits)
    db.session.add_all(grains)
    db.session.add_all(vegetables)
    db.session.add_all(orders)
    db.session.commit()
    print("Database seeding complete.")
