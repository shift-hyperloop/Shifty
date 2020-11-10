import sys
import os
from PyQt5 import QtCore, QtGui, QtQml
from functools import partial
import time
import queue
import threading
import random

q_RFID = queue.SimpleQueue()
q_barcode = queue.SimpleQueue()
q_distance = queue.SimpleQueue()


def threadfunc(q):
    time.sleep(3)
    q.put('Cola')
    time.sleep(6)
    q.put('Pepsi')
    time.sleep(0.5)
    q.put('Beer')
    time.sleep(0.5)
    q.put('Hookers')


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
    new_products = product_string.property("text") + barcode + "\n"
    product_string.clear()
    product_string.insert(0, new_products)

    # Get current price string, clear and update
    new_prices = price_string.property("text") + str(random.randint(10,1000)) + "\n"
    price_string.clear()
    price_string.insert(0, new_prices)


def check_inputs(engine):
    if q_RFID.qsize():
        pass

    if q_barcode.qsize():
        add_product(q_barcode.get(), engine)

    if q_distance.qsize():
        pass

 
def run():
    app = QtGui.QGuiApplication(sys.argv)
    myEngine = QtQml.QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, "main.qml")))

    threading.Thread(target=threadfunc, args=(q_barcode,), daemon=True).start()

    timer = QtCore.QTimer(interval=200)
    timer.timeout.connect(partial(check_inputs, myEngine))
    timer.start()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(run())
