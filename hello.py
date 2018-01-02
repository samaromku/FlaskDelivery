# coding=utf-8
import uuid

from datetime import datetime
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
# from flask_mysqldb import MySQL
import mysql.connector

# from flask_mysqldb import MySQL
# from flask.ext.mysql import MySQL

app = Flask(__name__)
conn = mysql.connector.connect(user='root', password='root', host='localhost', database='delivery')
cursor = conn.cursor(buffered=True)


@app.route('/')
def index():
    cursor.execute("INSERT INTO `delivery`.`user` (`name`, `email`) VALUES ('sam', 'hui@mail.ru')")
    conn.commit()
    cursor.execute('SELECT * FROM delivery.user')
    print cursor.fetchall()
    return "Привет, вы попали на главную страницу in ass!asd"


@app.route('/add_order', methods=['POST'])
def add_order():
    if (request.json):
        content = request.json
        print (content)
        title = content.get('title')
        description = content.get('description')
        address = content.get('address')

        # print (title, "title")
        # print (description, "description")
        # print (str(request.is_json))
        # created = datetime.now()
        # deadline = datetime.now()
        created = datetime.now()
        deadline = datetime.now()

        # from Order import Order
        # order = Order(title, description, created, deadline, address)
        # from database import add_order_in_db
        # add_order_in_db(order)

        cursor.execute("INSERT INTO delivery.order (title, description, address, created, deadline) "
                       "VALUES ('%s', '%s', '%s', '%s', '%s');" % (
                           title,
                           description,
                           address,
                           created,
                           deadline
                       ))

        conn.commit()
        last_id = cursor.lastrowid
        print (last_id)
        cursor.execute('SELECT * FROM delivery.order')
        return str(last_id)


@app.route('/auth')
def auth():
    # fixme сделать проверку имя и пароль из бд, если норм вернуть токен
    user_name = request.args.get('userName')
    password = request.args.get('password')
    result = {
        'token': uuid.uuid1()
    }
    app.logger.error('after %s', result)
    return jsonify(
        result
    )


@app.route('/get_current')
def get_current():
    current_orders_list = []
    for index in range(0, 10):
        current_orders_list.append({
            'id': index,
            'title': 'title order ' + str(index),
            'body': 'body order ' + str(index),
            'status': 1,
            'rating': 2,
            'createdDate': parse_date_from_db(datetime.now()),
            'deadLineDate': parse_date_from_db(datetime.now()),
            'url': 'http://'
        })
    return jsonify(current_orders_list)


# @app.before_request
# def log_request_info():
#     app.logger.error('Headers: %s', request.headers)
#     app.logger.error('Body: %s', request.get_data)
#     app.logger.error('args: %s', request.args)


@app.route('/kuzya', methods=['GET', 'POST'])
def kuzya():
    if request.method == 'POST':
        app.logger.debug('somthing i want to debug')
        return jsonify(
            user_name="kuzya",
            user_post="post loh")
    else:
        return jsonify("kuzya get loh")


def parse_date_from_db(db_date):
    if db_date == None: return
    return datetime.strftime(db_date, '%Y-%m-%dT%H:%M:%S')


if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(port=8999, debug=True)
