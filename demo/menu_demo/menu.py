# coding:utf-8
from typing import Union, List

from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QActionGroup, QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget
from qfluentwidgets import (
    RoundMenu as RM, Action, AvatarWidget, BodyLabel, CaptionLabel, setFont, HyperlinkButton, CheckableMenu,
    MenuIndicatorType, FluentIconBase, MenuAnimationType
)
from qfluentwidgets.components.material import AcrylicMenu as AM, AcrylicCheckableMenu


class MenuBase:

    def addItem(self, icon: Union[QIcon, str, FluentIconBase], text: str):
        """ add item to _menu"""
        action = Action(icon, text)
        self.addAction(action)
        return action

    def addItems(self, icon: List[Union[QIcon, str, FluentIconBase]], text: List[str]):
        """ add items to _menu"""
        actions = []
        for icon, text in zip(icon, text):
            actions.append(self.addItem(icon, text))
        return actions

    def setMenuMinWidth(self, width: int):
        self.setMinimumWidth(width)
        self.view.setMinimumWidth(width - 20)
        return self

    def setClickedSlot(self, action: Action, func):
        """ set click method """
        action.triggered.connect(func)
        return self

    def setShortcut(self, action: Action, key: str):
        """ set shortcut """
        action.setShortcut(QKeySequence(key))
        return self

    def centerExec(self, widget: QWidget, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        self.exec(widget.mapToGlobal(widget.rect().center()), ani, aniType)


class RoundMenu(MenuBase, RM):
    """ 菜单栏组件 """
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setMenuMinWidth(160)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicRoundMenu(MenuBase, AM):
    """ 亚力克菜单 """
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setMenuMinWidth(160)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class ProfileCardMenu(RoundMenu):
    """ 个人信息卡片组件 """
    def __init__(
            self,
            avatarPath: str,
            name: str,
            email: str,
            buttonText='主页',
            url='',
            parent=None
    ):
        super().__init__(parent)
        self._widget = QWidget()
        self._widget.setFixedSize(307, 82)
        self.addWidget(self._widget)
        self.addSeparator()
        self.__initCard(avatarPath, name, email, buttonText, url)

    def __initCard(self, avatarPath: str, name: str, email: str, buttonText: str, url: str = ''):
        self._avatar = AvatarWidget(avatarPath, self._widget)
        self._nameLabel = BodyLabel(name, self._widget)
        self._emailLabel = CaptionLabel(email, self._widget)
        self._button = HyperlinkButton(url, buttonText, self._widget)

        self._emailLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))
        self.setButtonFontSize(13)

        self.setAvatarRadius(24)
        self._avatar.move(3, 16)
        self._nameLabel.move(64, 13)
        self._emailLabel.move(64, 32)
        self._button.move(52, 48)

    def setButtonFontSize(self, size: int):
        setFont(self._button, size)
        return self

    def setAvatarMove(self, x: int, y: int):
        self._avatar.move(x, y)
        return self

    def setAvatarRadius(self, radius: int):
        self._avatar.setRadius(radius)
        return self

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicProfileCardMenu(ProfileCardMenu, AM):
    """ 亚力克个人信息卡片组件 """
    def __init__(self, avatarPath, name, email, buttonText="主页", url='', parent=None):
        super().__init__(avatarPath, name, email, buttonText, url, parent)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class CheckedMenu(MenuBase, CheckableMenu):
    """ 可选中菜单栏 """
    def __init__(self, title="", parent=None, indicatorType: MenuIndicatorType = MenuIndicatorType.CHECK):
        super().__init__(title, parent, indicatorType)
        self.setMenuMinWidth(160)
        self.g = QActionGroup(self)

    def enableChecked(self, enable: bool):
        if enable:
            for action in self.actions():
                print(True)
                self.g.addAction(action)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicCheckedMenu(CheckedMenu):
    def __init__(self, parent=None, indicatorType: MenuIndicatorType = MenuIndicatorType.CHECK):
        super().__init__(parent)
        self._menu = AcrylicCheckableMenu('', parent, indicatorType)


class Shortcut:
    """ 设置快捷键 """
    def addShortcut(self, key: str, parent: QWidget, function):
        """ set shortcut """
        shortcut = QShortcut(QKeySequence(key), parent)
        shortcut.activated.connect(function)
        return self

    def addShortcuts(self, keys: List[str], parent: QWidget, functions: List):
        for key, fc in zip(keys, functions):
            self.addShortcut(key, parent, fc)
        return self
