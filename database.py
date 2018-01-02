import mysql.connector

conn = mysql.connector.connect(user='root', password='root', host='localhost', database='delivery')
cursor = conn.cursor(buffered=True)


def add_order_in_db(order):
    print ("add_order")

    cursor.execute("INSERT INTO delivery.order (title, description, address, created, deadline) "
                   "VALUES ('%s', '%s', '%s', '%s', '%s');" % (
                       order.title,
                       order.description,
                       order.address,
                       order.created,
                       order.deadline
                   ))

    conn.commit()
    last_id = cursor.lastrowid
    print (last_id)
    cursor.execute('SELECT * FROM delivery.order')
    return last_id
