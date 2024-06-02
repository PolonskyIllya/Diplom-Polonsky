from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import date, timedelta
from models import db, User, ResortCity, TransportType
from flask_sqlalchemy import SQLAlchemy
from config import Config

# db.create_all()
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Словарь для хранения зарегистрированных пользователей
users = {
    "admin": "password123"
}

# Список курортных городов
resort_cities = [
    "Дубай", "Канкун", "Бали", "Гавайи", "Майями", "Париж", "Рим", "Барселона", "Токио", "Сидней", "Сен-Тропе", "Рио-де-Жанейро", "Тенерифе"
]

transport_types = ["Поезд", "Самолет", "Автобус"]

# Создаем пустую корзину
cart = []

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            return redirect(url_for('choose_destination'))
        else:
            error = 'Неверное имя пользователя или пароль. Попробуйте снова.'

    return render_template('login.html', error=error)

@app.route('/choose_destination', methods=['GET', 'POST'])
def choose_destination():
    if request.method == 'POST':
        destination = request.form['destination']
        transport_type = request.form['transport_type']
        travel_date = request.form['travel_date']
        return redirect(url_for('book_ticket', destination=destination, transport_type=transport_type, travel_date=travel_date))

    return render_template('destination.html', resort_cities=resort_cities, transport_type=transport_types)

@app.route('/book_ticket/<destination>/<transport_type>/<travel_date>', methods=['GET', 'POST'])
def book_ticket(destination, transport_type, travel_date):
    if request.method == 'POST':
        ticket_count = int(request.form['ticket_count'])
        total_cost = ticket_count * 1000  # Предположим, стоимость одного билета равна 1000 единицам

        # Добавляем товар в корзину
        item_id = f"{destination}-{transport_type}-{travel_date}"
        item_name = f"{destination} {transport_type} {travel_date}"
        item_price = 1000
        add_to_cart(item_id, item_name, item_price)

        return render_template('confirmation.html', destination=destination, transport_type=transport_type, travel_date=travel_date, ticket_count=ticket_count, total_cost=total_cost)

    return render_template('ticket.html', destination=destination, transport_type=transport_type, travel_date=travel_date)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart(item_id, item_name, item_price):
    # Ваша логика для добавления товара в корзину
    return redirect(url_for('cart'))

    
    # Проверяем, есть ли товар в корзине
    existing_item = next((item for item in cart if item['id'] == item_id), None)
    if existing_item:
        existing_item['quantity'] += 1
    else:
        # Создаем новый объект для добавления в корзину
        item = {'id': item_id, 'name': item_name, 'price': item_price, 'quantity': 1}
        cart.append(item)
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.form['item_id']
    
    # Находим объект в корзине и удаляем его
    for item in cart:
        if item['id'] == item_id:
            cart.remove(item)
            break
    
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/checkout')
def checkout():
    # Оформление заказа
    return 'Заказ оформлен'

if __name__ == '__main__':
    app.run(debug=True)

