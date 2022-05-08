import json


def get_users():
    with open('users.json', 'r', encoding='UTF-8') as file:
        list_users = json.load(file)
        return list_users


def get_orders():
    with open('orders.json', 'r', encoding='UTF-8') as file:
        list_orders = json.load(file)
        return list_orders


def get_offers():
    with open('offers.json', 'r', encoding='UTF-8') as file:
        list_offers = json.load(file)
        return list_offers


def users_to_dict(instance):
    """Преобразование в словарь"""
    return {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "age": instance.age,
        "email": instance.email,
        "role": instance.role,
        "phone": instance.phone,
    }


def orders_to_dict(instance):
    """Преобразование в словарь"""
    return {
        "id": instance.id,
        "name": instance.name,
        "description": instance.description,
        "start_date": instance.start_date,
        "end_date": instance.end_date,
        "address": instance.address,
        "price": instance.price,
        "customer_id": instance.customer_id,
        "executor_id": instance.executor_id
    }


def offers_to_dict(instance):
    """Преобразование в словарь"""
    return {
        "id": instance.id,
        "order_id": instance.order_id,
        "executor_id": instance.executor_id
    }

