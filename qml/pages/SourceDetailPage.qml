import QtQuick 2.0
import Sailfish.Silica 1.0


Page {
    id: page
    property var sourceItem
    property int index

    SilicaFlickable {
        anchors.fill: parent

        PullDownMenu {
            MenuItem {
                text: qsTr("Open hosts file URL")
                onClicked: Qt.openUrlExternally(sourceItem.url)
            }
            MenuItem {
                text: qsTr("More information")
                onClicked: Qt.openUrlExternally(sourceItem.info)
            }
        }

        contentHeight: column.height

        Column {
            id: column

            width: page.width
            spacing: Theme.paddingLarge
            PageHeader {
                title: sourceItem.name
            }
            Label {
                x: Theme.paddingLarge
                text: sourceItem.description
                color: Theme.secondaryHighlightColor
                font.pixelSize: Theme.fontSizeMedium
                wrapMode: Text.Wrap
                width: parent.width - 2*x
            }
            DetailItem {
                label: qsTr('Source')
                value: sourceItem.source
            }
            DetailItem {
                label: qsTr('License')
                value: sourceItem.license
            }
        }
    }
}

