import sys
import os
from PyQt5 import QtCore, QtGui, QtQml
from functools import partial
import queue
import requests
from post_request_test import request_product, request_user


q_shoppingCart = queue.SimpleQueue()


def mainWindow_setup(w):

    w.setTitle("ShiftKiosk")


def add_product(product, engine):
    # Check if window still open
    if not engine.rootObjects():
        return -1

    # Find product and price string in QML
    mainWindow = engine.rootObjects()[0]
    product_string = mainWindow.findChild(QtCore.QObject, "productString")
    price_string = mainWindow.findChild(QtCore.QObject, "priceString")

    # Find product name and price to be added
    product_name = product[0]
    product_price = product[1]
    product_stock = product[2]

    # Get current product string, clear and update
    new_products = product_string.property("text") + product_name + "\n"
    product_string.clear()
    product_string.insert(0, new_products)

    # Get current price string, clear and update
    new_prices = price_string.property("text") + product_price + "\n"
    price_string.clear()
    price_string.insert(0, new_prices)


def check_inputs(engine, q_cart):
    # Check for barcode input
    r = requests.get(url="http://192.168.1.132:5000/barcode")
    data = r.content.decode("utf-8")
    if data != "nothing new!":
        product = request_product(data)
        if len(product) > 1:
            add_product(product, engine)
            q_cart.put(product)
        else:
            add_product(["SEEK HELP","420","0"], engine) # TODO

    # Check for RFID input
    r = requests.get(url="http://192.168.1.132:5000/RFID")
    data = r.content.decode("utf-8")

    if data != "nothing new!":
        shopped_items = []
        loops = 0
        while q_cart.qsize():
            shopped_items.append(q_cart.get())
        for item in shopped_items:
            loops += int(item[1])

        user = request_user(data, amount_used=loops)
        if len(user) > 1:
            # Find product and price string in QML, and clear all the entries
            mainWindow = engine.rootObjects()[0]
            mainWindow.findChild(QtCore.QObject, "productString").clear()
            mainWindow.findChild(QtCore.QObject, "priceString").clear()
        else:
            add_product(["SEEK HELP",str(user[0]),"0"], engine) # TODO what to do if no user found?
            for item in shopped_items:
                q_cart.put(item)

    # Check for distance sensor stuff
    r = requests.get(url="http://192.168.1.132:5000/distance")
    data = r.content.decode("utf-8")
    if data != "nothing new!":
        if data == "del_last":
            pass
        elif data == "del_all":
            # Clear shopping queue in a thread safe way
            with q_cart.mutex:
                q_cart.queue.clear()
            # Find product and price string in QML, and clear all the entries
            mainWindow = engine.rootObjects()[0]
            mainWindow.findChild(QtCore.QObject, "productString").clear()
            mainWindow.findChild(QtCore.QObject, "priceString").clear()
        elif data == "easter_egg":
            pass


def run():
    app = QtGui.QGuiApplication(sys.argv)
    myEngine = QtQml.QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, "main.qml")))

    timer = QtCore.QTimer(interval=100)
    timer.timeout.connect(partial(check_inputs, myEngine, q_shoppingCart))
    timer.start()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(run())
