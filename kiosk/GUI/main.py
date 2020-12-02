import sys
import os
from PyQt5 import QtCore, QtGui, QtQml
from functools import partial
import queue
import requests
from request_methods import request_product_data, request_purchase
import datetime
import time


def mainWindow_setup(w):

    w.setTitle("ShiftKiosk")

def enter_idle_screen(engine):

    mainWindow = engine.rootObjects()[0]
    mainWindow.findChild(QtCore.QObject, "productString").clear()
    mainWindow.findChild(QtCore.QObject, "priceString").clear()
    mainWindow.findChild(QtCore.QObject, "totalstring").clear()
    mainWindow.findChild(QtCore.QObject, "userstring").clear().insert(0, "Scan a card or product to get started!")


def exit_idle_screen(engine):
    engine.rootObjects()[0].findChild(QtCore.QObject, "userstring").clear().insert(0, "Total:")


def update_total_price(engine):
    mainWindow = engine.rootObjects()[0]
    if mainWindow.findChild(QtCore.QObject, "pricestring"):
        price_string = mainWindow.findChild(QtCore.QObject, "pricestring").property("text")
        total_price_string = sum([int(x) for x in price_string.strip("\n").split("\n")]) # Splits string by "\n" into list, takes sum of list elements
        mainWindow.findChild(QtCore.QObject, "totalpricestring").clear().insert(total_price_string)


def add_product(product, engine):
    # Check if window still open
    if not engine.rootObjects():
        return -1

    # Find product and price string in QML
    mainWindow = engine.rootObjects()[0]
    product_string = mainWindow.findChild(QtCore.QObject, "productString")
    price_string = mainWindow.findChild(QtCore.QObject, "priceString")

    # Find product name and price to be added
    product_barcode = product[0]
    product_name = product[1]
    product_price = product[2]
    product_stock = product[3]

    # Get current product string, clear and update
    new_products = product_string.property("text") + product_name + "\n"
    product_string.clear()
    product_string.insert(0, new_products)

    # Get current price string, clear and update
    new_prices = price_string.property("text") + product_price + ",-\n"
    price_string.clear()
    price_string.insert(0, new_prices)


def query_barcode_scanner(engine, q_cart):

    while True:

        barcode = requests.get(url="http://192.168.1.132:5000/barcode").content.decode("utf-8")

        # If there are no more barcodes in the queue, let function complete
        if barcode == "nothing new!":
            break

        # If queue is not empty, add a product to the shopping basket
        else:
            product = [barcode] + request_product_data(barcode)
            if len(product) > 2:
                add_product(product, engine)
                q_cart.put(product)
            else:
                add_product(["SEEK HELP","420","0"], engine) # TODO


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

        elif data == "easter_egg": # TODO: Implement easter egg
            pass

    if delete_all:
        # Clear shopping queue in a thread safe way
        with q_cart.mutex:
            q_cart.queue.clear()
        # Find product and price string in QML, and clear all the entries
        mainWindow = engine.rootObjects()[0]
        mainWindow.findChild(QtCore.QObject, "productString").clear()
        mainWindow.findChild(QtCore.QObject, "priceString").clear()

    elif delete_last: # TODO: implement deleting last item
        pass


def query_rfid_scanner(engine, q_cart):

    response = requests.get(url="http://192.168.1.132:5000/RFID").content.decode("utf-8")

    if response != "nothing new!":
        mainWindow = engine.rootObjects()[0]
        mainWindow.findChild(QtCore.QObject, "productString").clear()
        mainWindow.findChild(QtCore.QObject, "priceString").clear()

        shopped_items = []
        totalPurchaseSum = 0
        while q_cart.qsize():
            shopped_items.append(q_cart.get())
        for item in shopped_items:
            totalPurchaseSum += int(item[2])

        user = request_purchase(response, purchaseSum=totalPurchaseSum)

        if len(user) > 1: # Money successfully subtracted from account

            # Subtract stock for purchased items
            for item in shopped_items:
                request_product_data(item[0], bought=1)
            # TODO: check for errors

            # Find product and price string in QML, and clear all the entries
            mainWindow = engine.rootObjects()[0]
            mainWindow.findChild(QtCore.QObject, "productString").clear()
            mainWindow.findChild(QtCore.QObject, "priceString").clear()

        elif user[0] == "ERROR: Balance too low for purchase":
            add_product(["SEEK HELP",str(user[1]),"0"], engine) # TODO what to do if no user found?
            for item in shopped_items:
                q_cart.put(item)
        elif user[0] == "ERROR: Invalid safety key.":
            # TODO: do stuff
            pass


def mainLoop(engine, q_cart):

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
    requests.get(url="http://192.168.1.132:5000/init") # Clears all the queues in the sensor suite

    timer = QtCore.QTimer(interval=100)
    timer.timeout.connect(partial(mainLoop, myEngine, q_shopping_cart))
    timer.start()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(run())
