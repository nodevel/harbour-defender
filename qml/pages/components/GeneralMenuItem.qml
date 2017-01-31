import QtQuick 2.0
import Sailfish.Silica 1.0

BackgroundItem {
    id: delegate

    Image {
        source: image
        anchors.centerIn: parent
    }

    Label {
        x: Theme.paddingLarge
        text: name
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            bottomMargin: Theme.paddingLarge
        }

        color: delegate.highlighted ? Theme.highlightColor : Theme.primaryColor
    }
    Rectangle {
        anchors.centerIn: parent
        width: parent.width - Theme.paddingMedium
        height: parent.height - Theme.paddingMedium
        opacity: delegate.highlighted ? 0.2 : 0.1
        color: delegate.highlighted ? Theme.highlightBackgroundColor : Theme.secondaryHighlightColor
    }

    onClicked: pageStack.push(Qt.resolvedUrl('../' + itemPage))
} // BackgroundItem
