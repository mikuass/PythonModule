# coding:utf-8
from typing import Union, List

from PySide6.QtGui import Qt, QIcon, QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget

from qfluentwidgets import (
    Pivot, SegmentedWidget, SegmentedToolWidget, SegmentedToggleToolWidget, FluentIconBase, TabBar,
    TabCloseButtonDisplayMode, PopUpAniStackedWidget, setTheme, Theme, HorizontalSeparator, FluentIcon,
    TransparentToolButton, Action
)

from ...common import setToolTipInfo
from ..layout import VBoxLayout, HBoxLayout
from .navigation_bar import NavigationBar, NavigationItemPosition
from ..widgets import Widget
from ..menu import Menu


class NavigationBase(Widget):
    """ 导航组件基类 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self.hBoxLayout = HBoxLayout(self)
        self.navigation = None
        self._key = '0'
        self.stackedWidget = PopUpAniStackedWidget(self)

    def _initLayout(self):
        self.vLayout = VBoxLayout(self)
        self.hLayout = HBoxLayout()
        self.hBoxLayout.addLayout(self.vLayout)
        self.vLayout.addWidgets([self.navigation, self.stackedWidget])
        self.vLayout.addLayout(self.hLayout)

    def addSeparator(self, index=1):
        separator = HorizontalSeparator(self)
        self.vLayout.insertWidget(index, separator)
        return self

    def addNavigationSeparator(self, index: int):
        self.navigation.insertItem(index, self._key, '|').setFixedWidth(1)
        self._key = str(int(self._key) + 1)
        return self

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
    ):
        """ add sub interface, rotKey isUnique"""
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(routeKey, text, lambda: self.switchTo(widget), icon)
        return self

    def addSubInterfaces(
            self,
            routeKeys: List[str],
            texts: List[str],
            widgets: List[QWidget],
            icons: List[Union[QIcon, str, FluentIconBase]] = None
    ):
        icons = icons if icons is not None else [None for _ in range(len(routeKeys))]
        for key, text, widget, icon in zip(routeKeys, texts, widgets, icons):
            self.addSubInterface(key, text, widget, icon)
        return self

    def switchTo(self, widget: QWidget):
        self.stackedWidget.setCurrentWidget(widget)

    def setCurrentItem(self, routeKey: str):
        self.navigation.setCurrentItem(routeKey)
        return self

    def enableNavCenter(self):
        self.vLayout.removeWidget(self.navigation)
        self.vLayout.insertWidget(0, self.navigation, alignment=Qt.AlignmentFlag.AlignHCenter)
        return self


class PivotNav(NavigationBase):
    """ 导航栏 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = Pivot(self)
        self._initLayout()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor('#2d2d2d'), 1, Qt.SolidLine))
        painter.drawLine(0, 65, self.width(), 60)


class SegmentedNav(PivotNav):
    """ 分段导航 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = SegmentedWidget(self)
        self._initLayout()

    def paintEvent(self, event):
        pass


class SegmentedToolNav(PivotNav):
    """ 工具导航 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = SegmentedToolWidget(self)
        self._initLayout()
        self.enableNavCenter()

    def addSubInterface(
            self,
            routeKey: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
    ):
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(routeKey, icon, lambda: self.switchTo(widget))
        return self

    def addSubInterfaces(
            self,
            routeKeys: List[str],
            widgets: List[QWidget],
            icons: List[Union[QIcon, str, FluentIconBase]]
    ):
        for key, widget, icon in zip(routeKeys, widgets, icons):
            self.addSubInterface(key, widget, icon)
        return self

    def paintEvent(self, event):
        pass


class SegmentedToggleToolNav(SegmentedToolNav):
    def __init__(self, parent=None):
        """ 主题色选中导航 """
        super().__init__(parent)
        self.navigation = SegmentedToggleToolWidget(self)
        self._initLayout()
        self.enableNavCenter()


class LabelBarWidget(Widget):
    """ 标签页组件 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tabBar = TabBar(self)
        self._stackedWidget = PopUpAniStackedWidget(self)
        self._hLayout = HBoxLayout(self)
        self._vLayout = VBoxLayout()
        self.__items = [] # type: List[QWidget]
        self.__initLayout()
        self.__initTitleBar()
        self.enableAddButton(False)

    def __initLayout(self):
        self._hLayout.addLayout(self._vLayout)
        self._vLayout.addWidgets([self._tabBar, self._stackedWidget])

    def __initTitleBar(self):
        self._tabBar.setTabShadowEnabled(True)
        self._tabBar.setMovable(True)
        self._tabBar.setScrollable(True)
        self._tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

    def setTabShadowEnabled(self, enable: bool):
        self._tabBar.setTabShadowEnabled(enable)

    def setMovable(self, movable: bool):
        self._tabBar.setMovable(movable)

    def setScrollable(self, scrollable: bool):
        self._tabBar.setScrollable(scrollable)

    def setCloseButtonDisplayMode(self, mode: TabCloseButtonDisplayMode):
        self._tabBar.setCloseButtonDisplayMode(mode)

    def enableClose(self):
        self._tabBar.tabCloseRequested.connect(lambda index: self.removeWidgetByIndex(index))


    def enableAddButton(self, enable: bool):
        if enable:
            self._tabBar.addButton.show()
            return
        self._tabBar.addButton.hide()

    def setCloseButtonDisplayMode(self, mode=TabCloseButtonDisplayMode.NEVER):
        self._tabBar.setCloseButtonDisplayMode(mode)

    def switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
    ):
        self._stackedWidget.addWidget(widget)
        self.__items.append(widget)
        widget.setProperty('text', text)
        widget.setProperty('routeKey', routeKey)
        self._tabBar.addTab(routeKey, text, icon, lambda: self.switchTo(widget))
        return widget

    def addSubInterfaces(
            self, routeKeys: List[str],
            texts: List[str],
            widgets: List[QWidget] = None,
            icons: List[Union[QIcon, str, FluentIconBase]] = None
    ):
        icons = icons if icons is not None else [None for _ in range(len(routeKeys))]
        for key, text, icon, widget in zip(routeKeys, texts, icons, widgets):
            self.addSubInterface(key, text, widget, icon)

    def removeWidgetByIndex(self, index: int):
        if index > len(self.__items):
            return
        item = self.__items.pop(index)
        self._stackedWidget.removeWidget(item)
        self._tabBar.removeTab(index)
        if index > 0:
            print(True)
            self._stackedWidget.setCurrentIndex(index - 1)

    def removeWidgetByName(self, widget: QWidget):
        if widget not in self.__items:
            return
        self.removeWidgetByIndex(self.__items.index(widget))


class SideNavigationWidget(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.__widgets = [] # type: List[QWidget]
        self._widgetLayout = HBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self._stackedWidget = PopUpAniStackedWidget(self)

        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.addWidget(self.navigationBar)
        self._widgetLayout.addWidget(self._stackedWidget)

    def enableReturn(self, enable: bool):
        self.navigationBar.enableReturn(enable)
        return self

    def expandNav(self):
        self.navigationBar.expandNav()
        return self

    def switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    def __addToStackedWidget(self, widget: QWidget):
        self._stackedWidget.addWidget(widget)
        self.__widgets.append(widget)

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            icon: Union[str, QIcon, FluentIconBase],
            widget: QWidget,
            position=NavigationItemPosition.SCROLL
    ):
        self.__addToStackedWidget(widget)
        self.navigationBar.addItem(routeKey, icon, text, False, lambda: self.switchTo(widget), position)
        return self

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        self.navigationBar.addSeparator(position)
        return self

    def insertSeparator(self, index: int, position=NavigationItemPosition.SCROLL):
        self.navigationBar.insertSeparator(index, position)
        return self

    def setCurrentWidget(self, routeKey: str):
        self.navigationBar.setCurrentItem(routeKey)
        return self

    def removeWidget(self, routeKey: str):
        self._stackedWidget.removeWidget(self.navigationBar.getWidget(routeKey))
        self.navigationBar.removeWidget(routeKey)

    def getAllWidget(self):
        return self.__widgets