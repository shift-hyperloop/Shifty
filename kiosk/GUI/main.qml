import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    width: 1500
    height: 1000
    visible: true
    title: qsTr("Hello World")
    objectName: "Main Window"

    Text {
        id: title
        x: parent.width/2 - this.width/2
        y: 29
        width: 700
        height: 74
        color: "#0090d8"
        text: qsTr("Welcome to the Shift Shop!")
        font.pixelSize: 54
        font.family: "MontSerrant"
        font.bold: true
        fontSizeMode: Text.FixedSize
        objectName: "Title"
    }

    Rectangle {
        id: rectangle
        x: 0
        y: 97
        width: 1500
        height: 903
        color: "#ffffff"
        objectName: "Rectangle"

        Column {
            id: itemList
            x: 172
            y: 128
            width: 709
            height: 775
            padding: 0
            objectName: "Left Column"

            TextEdit {
                id: productString
                width: 400
                text: ""
                anchors.right: parent.right
                horizontalAlignment: Text.AlignRight
                font.pointSize: 18
                objectName: "productString"
            }


        }

        Column {
            id: priceList
            x: 930
            y: 128
            width: 320
            height: 775
            objectName: "Right Column"

            TextEdit {
                width: 100
                text: ""
                font.pointSize: 18
                objectName: "priceString"
            }
        }

        TextEdit {
            id: userstring
            objectName: "userstring"
            x: 446
            y: 55
            width: 435
            height: 67
            horizontalAlignment: Text.AlignRight
            text: ""
            font.pixelSize: 18
        }

        TextEdit {
            id: totalpricestring
            objectName: "totalpricestring"
            x: 930
            y: 55
            width: 266
            height: 67
            text: ""
            font.pixelSize: 12
        }


        }
    }



/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}
}
##^##*/
