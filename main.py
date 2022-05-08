from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils import users_to_dict, orders_to_dict, offers_to_dict, get_users, get_offers, get_orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#  !!!!!!!!!!!!!!!!!!! ПОЛЯ КЛАССА User !!!!!!!!!!!!!!!!!!!
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100))
    role = Column(String(50))
    phone = Column(String(50))

    def transformation_to_dict(self, data):  # Чтобы не указывать поля в методе PUT.
        for k, v in data.items():            # Примает данные и записывает в определенное поле
            setattr(self, k, v)

#  !!!!!!!!!!!!!!!!!!! ПОЛЯ КЛАССА Orders !!!!!!!!!!!!!!!!!!!
class Orders(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(500))
    start_date = Column(String(50))
    end_date = Column(String(50))
    address = Column(String(150))
    price = Column(Integer)
    customer_id = Column(Integer, ForeignKey('users.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))
    customer = relationship('User', foreign_keys=[customer_id])
    executor = relationship('User', foreign_keys=[executor_id])

    def transformation_to_dict(self, data):
        for k, v in data.items():
            setattr(self, k, v)


#  !!!!!!!!!!!!!!!!!!! ПОЛЯ КЛАССА Offers !!!!!!!!!!!!!!!!!!!
class Offers(db.Model):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    executor_id = Column(Integer, ForeignKey('users.id'))
    orders = relationship('Orders')
    executor = relationship('User')

    def transformation_to_dict(self, data):
        for k, v in data.items():
            setattr(self, k, v)


# db.drop_all() Удаление таблиц
db.create_all()  # Создание таблиц


# !!!!!!!!!!!!!!!!!!! ДОБВЛЯЮ ДАННЫЕ В ПОЛЯ ТАБЛИЦЫ USERS ИЗ JSON !!!!!!!!!!!!!!!!!
all_users = []

list_user = get_users()
for i in range(len(list_user)):
    user = User(id=list_user[i]['id'],
                first_name=list_user[i]['first_name'],
                last_name=list_user[i]['last_name'],
                age=list_user[i]['age'],
                email=list_user[i]['email'],
                role=list_user[i]['role'],
                phone=list_user[i]['phone']
                )
    all_users.append(user)

db.session.add_all(all_users)


# !!!!!!!!!!!!!!!!!!! ДОБВЛЯЮ ДАННЫЕ В ПОЛЯ ТАБЛИЦЫ ORDERS ИЗ JSON !!!!!!!!!!!!!!!!!
all_orders = []

list_orders = get_orders()
for i in range(len(list_orders)):
    order = Orders(id=list_orders[i]['id'],
                   name=list_orders[i]['name'],
                   description=list_orders[i]['description'],
                   start_date=list_orders[i]['start_date'],
                   end_date=list_orders[i]['end_date'],
                   address=list_orders[i]['address'],
                   price=list_orders[i]['price'],
                   customer_id=list_orders[i]['customer_id'],
                   executor_id=list_orders[i]['executor_id']
                   )
    all_orders.append(order)

db.session.add_all(all_orders)


# !!!!!!!!!!!!!!!!!!! ДОБВЛЯЮ ДАННЫЕ В ПОЛЯ ТАБЛИЦЫ OFFERS ИЗ JSON !!!!!!!!!!!!!!!!!
all_offers = []

list_offers = get_offers()
for i in range(len(list_offers)):
    offer = Offers(id=list_offers[i]['id'],
                   order_id=list_offers[i]['order_id'],
                   executor_id=list_offers[i]['executor_id']
                   )
    all_offers.append(offer)

db.session.add_all(all_offers)
db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        users_list = []
        users = User.query.all()
        for user in users:
            users_list.append(users_to_dict(user))
        return jsonify(users_list)
    elif request.method == 'POST':
        data = request.json  # принимает данные из Postman
        with db.session.begin():
            user = User(**data)  # создаем объект класса (**data = данные из Postman)
            db.session.add(user)  # добвляем объект
        return jsonify(users_to_dict(user))


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_one_user(uid):
    if request.method == 'GET':
        user_list = []
        user = User.query.get(uid)
        user_list.append(users_to_dict(user))
        return jsonify(user_list)
    elif request.method == 'PUT':
        data = request.json
        with db.session.begin():
            user = User.query.filter(User.id == uid).one()
            user.transformation_to_dict(data)
            return jsonify(users_to_dict(user))
    elif request.method == 'DELETE':
        with db.session.begin():
            User.query.filter(User.id == uid).delete()
            return redirect('/users')


@app.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'GET':
        orders_list = []
        orders = Orders.query.all()
        for order in orders:
            orders_list.append(orders_to_dict(order))
        return jsonify(orders_list)
    elif request.method == 'POST':
        data = request.json
        with db.session.begin():
            order = Orders(**data)
            db.session.add(order)
        return jsonify(orders_to_dict(order))


@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def get_orders(oid):
    if request.method == 'GET':
        orders_list = []
        order = Orders.query.get(oid)
        orders_list.append(orders_to_dict(order))
        return jsonify(orders_list)
    elif request.method == 'PUT':
        data = request.json
        with db.session.begin():
            order = Orders.query.filter(Orders.id == oid).one()
            order.transformation_to_dict(data)
            return jsonify(orders_to_dict(order))
    elif request.method == 'DELETE':
        with db.session.begin():
            Orders.query.filter(Orders.id == oid).delete()
            return redirect('/orders')


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        offers_list = []
        offers = Offers.query.all()
        for offer in offers:
            offers_list.append(offers_to_dict(offer))
        return jsonify(offers_list)
    elif request.method == 'POST':
        data = request.json
        with db.session.begin():
            offer = Offers(**data)
            db.session.add(offer)
        return jsonify(offers_to_dict(offer))


@app.route('/offers/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def get_one_offer(oid):
    if request.method == 'GET':
        offers_list = []
        offer = Offers.query.get(oid)
        offers_list.append(offers_to_dict(offer))
        return jsonify(offers_list)
    elif request.method == 'PUT':
        data = request.json
        with db.session.begin():
            offer = Offers.query.filter(Offers.id == oid).one()
            offer.transformation_to_dict(data)
            return jsonify(offers_to_dict(offer))
    elif request.method == 'DELETE':
        with db.session.begin():
            Offers.query.filter(Offers.id == oid).delete()
            return redirect('/offers')


if __name__ == '__main__':
    app.run()
