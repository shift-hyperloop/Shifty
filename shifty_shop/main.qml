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
            x: 175
            y: 40
            width: 709
            height: 775
            padding: 0
            objectName: "Left Column"

            TextEdit {
                id: priceString
                anchors.right: parent.right
                horizontalAlignment: Text.AlignRight
                font.pointSize: 18
                objectName: "PriceString"
            }

            /*TextEdit {
                id: priCeString
                x: 695
                y: 107
                width: 189
                height: 98
                text: qsTr("Text Edit")
                font.pixelSize: 18
                horizontalAlignment: Text.AlignRight
                verticalAlignment: Text.AlignTop
                */


        }

        Column {
            id: priceList
            x: 933
            y: 40
            width: 320
            height: 775
            objectName: "Right Column"

            Text {
                text: "69kr\n"
                font.pointSize: 18
                objectName: "Price List"
            }
        }


        }
    }



/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}
}
##^##*/
