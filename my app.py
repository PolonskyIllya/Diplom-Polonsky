from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta
# from models import db, User, ResortCity, TransportType


app = Flask(__name__)

# Словарь для хранения зарегистрированных пользователей
users = {
    "admin": "password123"
}

# Список курортных городов
resort_cities = [
    "Дубай", "Канкун", "Бали", "Гавайи", "Майями", "Париж", "Рим", "Барселона", "Токио", "Сидней", "Сен-Тропе", "Рио-де-Жанейро", "Тенерифе"
]

transport_types = ["Поезд", "Самолет", "Автобус"]

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
        return render_template('confirmation.html', destination=destination, transport_type=transport_type, travel_date=travel_date, ticket_count=ticket_count, total_cost=total_cost)

    return render_template('ticket.html', destination=destination, transport_type=transport_type, travel_date=travel_date)

if __name__ == '__main__':
    app.run(debug=True)
