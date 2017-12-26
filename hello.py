import uuid

from datetime import datetime
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler

# from flask_mysqldb import MySQL
# from flask.ext.mysql import MySQL

app = Flask(__name__)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run()


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


@app.before_request
def log_request_info():
    app.logger.error('Headers: %s', request.headers)
    app.logger.error('Body: %s', request.get_data)
    app.logger.error('args: %s', request.args)


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