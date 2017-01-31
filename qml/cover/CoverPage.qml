import QtQuick 2.0
import Sailfish.Silica 1.0

CoverBackground {

    Column {
        width: parent.width
        anchors {
            horizontalCenter: parent.horizontalCenter
            top: parent.top
            topMargin: Theme.paddingLarge
        }
        DetailItem {
            label: qsTr("Last")
            value: (stats.last_time > 0) ? stats.last_time.toLocaleTimeString() : '?'
            anchors.horizontalCenter: parent.horizontalCenter
        }
        DetailItem {
            label: qsTr("Enabled")
            value: (stats.last_sources > 0) ? qsTr('Yes') : qsTr('No')
            anchors.horizontalCenter: parent.horizontalCenter
        }
        Label {
            x: Theme.paddingLarge
            text: appName
            color: Theme.primaryColor
            anchors.horizontalCenter: parent.horizontalCenter
        }
    } // Column

//    CoverActionList {
//        id: coverAction

//        CoverAction {
//            iconSource: "image://theme/icon-cover-next"
//        }

//        CoverAction {
//            iconSource: "image://theme/icon-cover-pause"
//        }
//    }
}

