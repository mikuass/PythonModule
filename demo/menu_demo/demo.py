# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from FluentWidgets import SideNavigationWidget, Widget
from qfluentwidgets import FluentIcon, TitleLabel

from menu import RoundMenu, AcrylicRoundMenu, ProfileCardMenu, AcrylicProfileCardMenu, CheckedMenu, AcrylicCheckedMenu


class Window(SideNavigationWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu = AcrylicProfileCardMenu(r"C:\Users\Administrator\OneDrive\Pictures\1734703508871.jpg", 'name', 'email', 'homepage', 'https://www.bilibili.com', self)
        self.menu = CheckedMenu(self)
        self.menuWidget1 = SubWidget(
            self, "Menu Widget1",
            self.menu
        )
        self.menuWidget2 = SubWidget(
            self, 'Menu Widget2',
            self.menu
        )

        self.initNavigation()

        self.menu.addItem(FluentIcon.HOME, 'item1')
        self.menu.addItem(FluentIcon.GITHUB, 'item2')
        self.menu.addItem(FluentIcon.SETTING, 'item3')
        self.menu.addSeparator()
        self.menu.addItem(FluentIcon.COPY, 'copy')
        self.menu.addItem(FluentIcon.CUT, 'cut')
        self.menu.addItem(FluentIcon.PASTE, 'past')

        # self.menu.removeAction(i3)

        for item in self.navigationBar.getAllWidget().values():
            item.setSelectedColor('orange')

        self.menu.addToGroup(self.menu.actions()[:3])

    def initNavigation(self):
        self.addSubInterface(
            'menu1',
            'Menu',
            FluentIcon.APPLICATION,
            self.menuWidget1
        )
        self.addSubInterface(
            'menu2',
            'Menu',
            FluentIcon.GITHUB,
            self.menuWidget2
        )
        self.setCurrentWidget('menu2')


class SubWidget(Widget):
    def __init__(self, parent=None, text=None, menu=None):
        super().__init__(parent)
        TitleLabel(text, self)
        self.menu = menu

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        # self.menu.centerExec(self)
        self.menu.exec(event.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())