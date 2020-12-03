import sys
import os
import time
import queue

from PyQt5 import QtCore, QtGui, QtQml
from functools import partial

from request_methods import *




def enter_idle_screen(engine):

    mainWindow = engine.rootObjects()[0]
    mainWindow.findChild(QtCore.QObject, "productString").clear()
    mainWindow.findChild(QtCore.QObject, "priceString").clear()
    mainWindow.findChild(QtCore.QObject, "totalpricestring").clear()
    mainWindow.findChild(QtCore.QObject, "userstring").clear()
    mainWindow.findChild(QtCore.QObject, "userstring").insert(0, "Scan a card or product to get started!")


def exit_idle_screen(engine):

    engine.rootObjects()[0].findChild(QtCore.QObject, "userstring").clear().insert(0, "Total:")


def update_total_price(engine):

    mainWindow = engine.rootObjects()[0]
    if mainWindow.findChild(QtCore.QObject, "pricestring"):
        price_string = mainWindow.findChild(QtCore.QObject, "pricestring").property("text")
        total_price_string = sum([int(x) for x in price_string.strip("\n").split("\n")])  # Splits string by "\n" into list, takes sum of list elements
        mainWindow.findChild(QtCore.QObject, "totalpricestring").clear().insert(total_price_string)


def basket_add(product, engine, q_cart):

    # Find product and price string in QML
    mainWindow = engine.rootObjects()[0]
    product_string = mainWindow.findChild(QtCore.QObject, "productString")
    price_string = mainWindow.findChild(QtCore.QObject, "priceString")

    # Find product name and price to be added
    product_barcode = product[0]
    product_name = product[1]
    product_price = product[2]

    # Get current product string, clear and update
    new_products = product_string.property("text") + product_name + "\n"
    product_string.clear()
    product_string.insert(0, new_products)

    # Get current price string, clear and update
    new_prices = price_string.property("text") + product_price + ",-\n"
    price_string.clear()
    price_string.insert(0, new_prices)

    q_cart.put(product)


# TODO: Implement deleting last cart entry
def basket_delete_last(engine, q_cart):
    return NotImplementedError('Deleting last entry not yet implemented')


def basket_delete_all(engine, q_cart):

    # Clear shopping queue in a thread-safe way
    with q_cart.mutex:
        q_cart.queue.clear()

    # Find product and price string in QML, and clear all the entries
    mainWindow = engine.rootObjects()[0]
    mainWindow.findChild(QtCore.QObject, "productString").clear()
    mainWindow.findChild(QtCore.QObject, "priceString").clear()


def query_barcode_scanner(engine, q_cart):

    while True:

        response = requests.get(url="http://192.168.1.132:5000/barcode").content.decode("utf-8")

        # If there are no more barcodes in the queue, let function complete
        if response == "nothing new!":
            break

        # If queue is not empty, request product data from the django database
        else:
            product = get_product_data(response)

            # If a list with more than one entry is returned, the product exists in the database. Add to basket.
            if len(product) > 1:
                basket_add(product, engine, q_cart)

            # Product did not exist in the database, TODO: inform that product was added to DB as {product[0]}.
            elif -300 <= int(product[0]) <= -100:
                pass

            # Something else went wrong. TODO: inform customer that (s)he is fucked. Play mocking sound.
            elif int(product[0]) == -1:
                pass


def query_distance_sensor(engine, q_cart):

    delete_last = False
    delete_all = False

    while True:

        data = requests.get(url="http://192.168.1.132:5000/distance").content.decode("utf-8")

        if data == "nothing new!":
            break

        elif data == "del_last":
            delete_last = True

        elif data == "del_all":
            delete_all = True

        elif data == "easter_egg":  # TODO: Wilhelm scream?
            pass

    if delete_all:
        basket_delete_all(engine, q_cart)

    elif delete_last:
        basket_delete_last(engine, q_cart)


def query_rfid_scanner(engine, q_cart):

    response = requests.get(url="http://192.168.1.132:5000/RFID").content.decode("utf-8")

    if response != "nothing new!":

        user = get_user_data(response)

        if type(user) != list:
            pass
            # TODO: Show user that he was added to database with the id {user}

        else:
            user_rfid = user[0]
            user_name = user[1]
            balance = int(user[2])

            shopped_items = []
            list_of_barcodes = []
            tot_purchase_sum = 0
            while q_cart.qsize():
                shopped_items.append(q_cart.get())
            for item in shopped_items:
                list_of_barcodes.append(item[0])
                tot_purchase_sum += int(item[2])

            if balance >= tot_purchase_sum:
                result = post_purchase_order(user_rfid, list_of_barcodes, tot_purchase_sum)

                if not result:  # Unsuccessful purchase
                    for item in shopped_items:
                        q_cart.put(item)

                else:  # Successful purchase
                    mainWindow = engine.rootObjects()[0]
                    mainWindow.findChild(QtCore.QObject, "productString").clear()
                    mainWindow.findChild(QtCore.QObject, "priceString").clear()

                    balancestring = mainWindow.findChild(QtCore.QObject, "totalpricestring")
                    balancestring.clear()
                    balancestring.insert(0, "Remaining balance: " + str(balance))

                    userstring = mainWindow.findChild(QtCore.QObject, "userstring")
                    userstring.clear()
                    userstring.insert(0, "Purchase complete! Charged " + str(tot_purchase_sum)+ ",-")

                    for i in range(90000000):
                        if i == 89999999:
                            enter_idle_screen(engine)
                        

def main_loop(engine, q_cart):

    query_barcode_scanner(engine, q_cart)
    query_distance_sensor(engine, q_cart)
    query_rfid_scanner(engine, q_cart)
    update_total_price(engine)


def run():

    app = QtGui.QGuiApplication(sys.argv)
    myEngine = QtQml.QQmlApplicationEngine(parent=app)
    directory = os.path.dirname(os.path.abspath(__file__))
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, "main.qml")))

    q_shopping_cart = queue.Queue()

    attempts = 0
    while True:
        try:
            requests.get(url="http://192.168.1.132:5000/init")  # Clears all the queues in the sensor suite
            break
        except ConnectionError:
            attempts += 1
            # TODO: Visual or audio response that connection failed?
            if attempts > 2:
                sys.exit()
            time.sleep(10)

    timer = QtCore.QTimer(interval=100)
    timer.timeout.connect(partial(main_loop, myEngine, q_shopping_cart))
    timer.start()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(run())
