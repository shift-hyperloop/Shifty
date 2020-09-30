import urllib.request

from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class ShopItem(QWidget):

    def __init__(self, uuid, name, price, image_url):
        super(ShopItem, self).__init__()

        self.id = uuid
        self.name = name
        self.price = price
        self.image_url = image_url

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        url = self.image_url
        data = urllib.request.urlopen(url).read()

        image = QImage()
        image.loadFromData(data)

        lbl = QLabel(self)
        lbl.setPixmap(QPixmap(image))

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.show()
    



