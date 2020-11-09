
# Imports
import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui, QtQml
from functools import partial
import time
import queue


q_RFID = queue.SimpleQueue()
q_barcode = queue.SimpleQueue()
q_distance = queue.SimpleQueue()


q_barcode.put("837456")
q_barcode.put("894753")


def mainWindow_setup(w):

    w.setTitle("ShiftKiosk")


def add_product(barcode, engine):
    # Check if window still open
    if not engine.rootObjects():
        return -1

    # Find product and price string in QML
    mainWindow = engine.rootObjects()[0]
    product_string = mainWindow.findChild(QtCore.QObject, "productString")
    price_string = mainWindow.findChild(QtCore.QObject, "priceString")

    # Find product name and price to be added
    product_name = "Red Knull"
    product_price = "69 (neida egt 17) kr"

    # Get current product string, clear and update
    new_products = product_string.property("text") + product_name + "\n"
    product_string.clear()
    product_string.insert(0, new_products)

    # Get current price string, clear and update
    new_prices = price_string.property("text") + product_price + "\n"
    price_string.clear()
    price_string.insert(0, new_prices)


def run():
    app = QtGui.QGuiApplication(sys.argv)
    myEngine = QtQml.QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, "main.qml")))

    if q_RFID.qsize():
        pass

    if q_barcode.qsize():
        add_product(q_barcode.get(), myEngine)

    if q_distance.qsize():
        pass

    return app.exec_()


if __name__ == "__main__":
    sys.exit(run())






