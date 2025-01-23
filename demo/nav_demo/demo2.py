# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from docutils.nodes import title
from qfluentwidgets import FluentIcon, TitleLabel, PushButton

from FluentWidgets import SideNavigationWidget, NavigationItemPosition, LabelBarWidget, SegmentedToolNav, PivotNav


class NavigationDemo(LabelBarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 520)

        self._tabBar.addScrollBarWidget(TitleLabel("TEST", self), Qt.AlignmentFlag.AlignLeft)

        self.addSubInterface(
            'HOME',
            "HOME",
            TitleLabel("HOME", self),
            FluentIcon.HOME,
        )
        self.addSubInterface(
            "GITHUB",
            "GITHUB",
            TitleLabel("GITHUB", self),
            FluentIcon.GITHUB,
        )
        self.addSubInterface(
            "SETTING",
            "SETTING",
            TitleLabel("SETTING", self),
            FluentIcon.SETTING,
        )
        self.addSubInterface(
            "ABOUT",
            "ABOUT",
            TitleLabel("ABOUT", self),
            FluentIcon.INFO
        )
        self.addSubInterface(
            "MUSIC",
            "MUSIC",
            TitleLabel("MUSIC", self),
            FluentIcon.MUSIC
        )

        self.enableClose()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = NavigationDemo()
    demo.show()
    sys.exit(app.exec())