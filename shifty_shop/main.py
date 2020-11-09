
# Imports
import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui, QtQml
from functools import partial
import time
#from PySide2.QtUiTools import QUiLoader

#loader = QUiLoader()


def mainWindow_setup(w):

    w.setTitle("ShiftKiosk")

def add_product(r):
    scanned = input("Scann vare eller kort: ")
    r.append(scanned)


def run():
    app = QtGui.QGuiApplication(sys.argv)
    myEngine = QtQml.QQmlApplicationEngine()
    directory = os.path.dirname(os.path.abspath(__file__))
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, "main.qml")))
    if not myEngine.rootObjects():
        return -1
    mainWindow = myEngine.rootObjects()[0]
    text = mainWindow.findChild(QtCore.QObject, "PriceString")
    print(text)
    timer = QtCore.QTimer(interval=500)
    timer.timeout.connect(partial(add_product, text))
    timer.start()
    return app.exec_()



if __name__ == "__main__":
    sys.exit(run())






