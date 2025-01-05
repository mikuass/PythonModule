# coding:utf-8
from PySide6.QtGui import QColor, QPainter

from ..layout import VBoxLayout, HBoxLayout
from PySide6.QtWidgets import QFrame, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize
from qfluentwidgets import FluentIcon, TransparentToolButton, SubtitleLabel, setTheme, Theme, qconfig


class PopDrawerWidgetBase(QFrame):
    """ pop drawer widget base """
    def __init__(
            self,
            parent,
            title='弹出抽屉',
            aniType=QEasingCurve.Type.Linear,
            duration=250,
            width: int = None,
            height: int = None,
            lightBackgroundColor=QColor('#ECECEC'),
            darkBackgroundColor=QColor('#202020'),
            xRadius=10,
            yRyRadius=10
    ):
        super().__init__(parent)
        # Linear
        # InBack
        setTheme(Theme.AUTO)
        self.parent = parent
        self.aniType = aniType
        self.duration = duration
        self._width = width or 300
        self._height = height or parent.height()
        self.__xRadius = xRadius
        self.__yRadius = yRyRadius
        self.__lightBgcColor = lightBackgroundColor
        self.__darkBgcColor = darkBackgroundColor
        self.__animation = None
        self.__title = SubtitleLabel(title, self)
        self.__closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.__closeButton.setIconSize(QSize(12, 12))
        self.__closeButton.clicked.connect(self.hideDrawer)
        self.setFixedSize(self._width, self._height)
        self.hide()
        self.__initLayout()

    def __initLayout(self):
        self.__vBoxLayout = VBoxLayout(self)
        self.__hBoxLayout = HBoxLayout(self)
        self.__vBoxLayout.insertLayout(0, self.__hBoxLayout)
        self.__vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__hBoxLayout.addWidget(self.__title)
        self.__hBoxLayout.addWidget(self.__closeButton, alignment=Qt.AlignmentFlag.AlignRight)

    def addWidget(self, widget: QWidget):
        """ add widget to layout """
        self.__vBoxLayout.addWidget(widget)
        return self

    def setTitleText(self, text: str):
        self.__title.setText(text)

    def __dockAnimation(self, startPoint: QPoint, endPoint: QPoint):
        self.__animation = QPropertyAnimation(self, b'pos')
        self.__animation.setEasingCurve(self.aniType)
        self.__animation.setDuration(self.duration)
        self.__animation.setStartValue(startPoint)
        self.__animation.setEndValue(endPoint)
        self.__animation.start()

    def showDrawer(self, x: QPoint, y: QPoint):
        """ show dock, dock visible """
        if self.isVisible():
            self.hideDrawer()
            return
        self.setVisible(True)
        self.__dockAnimation(x, y)

    def hideDrawer(self, x: QPoint, y: QPoint):
        """ hide dock, dock not visible """
        if self.isVisible():
            self.__dockAnimation(x, y)
        QTimer.singleShot(self.duration, lambda: self.setVisible(False))

    def setRoundRadius(self, xRadius: int, yRadius: int):
        self.__xRadius = xRadius
        self.__yRadius = yRadius
        self.update()

    def setBackgroundColor(self, lightColor: QColor, darkColor: QColor):
        self.__lightBgcColor = lightColor
        self.__darkBgcColor = darkColor
        self.update()

    def getBackgroundColor(self):
        if qconfig.theme == Theme.DARK:
            return self.__darkBgcColor
        else:
            return self.__lightBgcColor

    def getXRadius(self):
        return self.__xRadius

    def getYRadius(self):
        return self.__yRadius

    def mousePressEvent(self, event):
        # 阻止事件传递给父类控件
        event.accept()

    def resizeEvent(self, event):
        """ 父类须在 resizeEvent 调用本类的 resizeEvent 方法"""
        self.setFixedSize(self._width, self.parent.height())

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())


class LeftPopDrawerWidget(PopDrawerWidgetBase):
    """ left pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            aniType=QEasingCurve.Type.Linear,
            duration=250,
            width: int = None,
            height: int = None,
            lightBackgroundColor=QColor('#ECECEC'),
            darkBackgroundColor=QColor('#202020'),
            xRadius=10,
            yRyRadius=10
    ):
        super().__init__(
            parent, title, aniType, duration, width, height,
            lightBackgroundColor,darkBackgroundColor, xRadius, yRyRadius
        )

    def showDrawer(self):
        super().showDrawer(QPoint(-self.width(), 0), QPoint(0, 0))

    def hideDrawer(self):
        super().hideDrawer(QPoint(0, 0), QPoint(-self.width(), 0))


class RightPopDrawerWidget(PopDrawerWidgetBase):
    """ right pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            aniType=QEasingCurve.Type.Linear,
            duration=250,
            width: int = None,
            height: int = None,
            lightBackgroundColor=QColor('#ECECEC'),
            darkBackgroundColor=QColor('#202020'),
            xRadius=10,
            yRyRadius=10
    ):
        super().__init__(
            parent, title, aniType, duration, width, height,
            lightBackgroundColor, darkBackgroundColor, xRadius, yRyRadius
        )

    def showDrawer(self):
        super().showDrawer(
            QPoint(self.parent.width() + self.width(), 0),
            QPoint(self.parent.width() - self.width(), 0)
        )

    def hideDrawer(self):
        super().hideDrawer(
            QPoint(self.parent.width() - self.width(), 0),
            QPoint(self.parent.width() + self.width(), 0)
        )


class TopPopDrawerWidget(PopDrawerWidgetBase):
    """ top pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            aniType=QEasingCurve.Type.Linear,
            duration=250,
            width: int = None,
            height: int = None,
            lightBackgroundColor=QColor('#ECECEC'),
            darkBackgroundColor=QColor('#202020'),
            xRadius=10,
            yRyRadius=10
    ):
        super().__init__(
            parent, title, aniType, duration, width, height or 250,
            lightBackgroundColor, darkBackgroundColor, xRadius, yRyRadius
        )

    def showDrawer(self):
        super().showDrawer(QPoint(0, -self.height()), QPoint(0, 0))

    def hideDrawer(self):
        super().hideDrawer(QPoint(0, 0), QPoint(0, -self.height()))

    def resizeEvent(self, event):
        self.setFixedSize(self.parent.width(), self._height)


class BottomPopDrawerWidget(PopDrawerWidgetBase):
    """ bottom pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            aniType=QEasingCurve.Type.Linear,
            duration=250,
            width: int = None,
            height: int = None,
            lightBackgroundColor=QColor('#ECECEC'),
            darkBackgroundColor=QColor('#202020'),
            xRadius=10,
            yRyRadius=10
    ):
        super().__init__(
            parent, title, aniType, duration, width, height or 250,
            lightBackgroundColor, darkBackgroundColor, xRadius, yRyRadius
        )

    def showDrawer(self):
        super().showDrawer(
            QPoint(0, self.parent.height() + self.height()),
            QPoint(0, self.parent.height() - self.height())
        )

    def hideDrawer(self):
        super().hideDrawer(
            QPoint(0, self.parent.height() - self.height()),
            QPoint(0, self.parent.height() + self.height())
        )

    def resizeEvent(self, event):
        self.setFixedSize(self.parent.width(), self._height)