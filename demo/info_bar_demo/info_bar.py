# coding:utf-8
from enum import Enum
from typing import Union

from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QObject, QEvent, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect, QWidget
from qfluentwidgets import BodyLabel, TransparentToolButton, FluentIcon, SubtitleLabel, isDarkTheme

from ...components import VBoxLayout, HBoxLayout


class ToastInfoBarColor(Enum):
    """ toast infoBar color """
    SUCCESS = '#4CAF50'
    ERROR = '#FF5733'
    WARNING = '#FFEB3B'
    INFO = '#2196F3'

    def __new__(cls, color):
        obj = object.__new__(cls)
        obj.color = QColor(color)
        return obj

    @property
    def value(self):
        return self.color


class ToastInfoBarPosition(Enum):
    """ toast infoBar position """
    TOP = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5


class ToastInfoBar(QFrame):
    """ toast infoBar """
    closeSignal = Signal()

    def __init__(
            self,
            parent,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_LEFT,
            toastColor: QColor | ToastInfoBarColor = ToastInfoBarColor.SUCCESS,
            isCustomBgcColor=False,
            bgcColor=None
    ):
        super().__init__(parent)
        self.parent().installEventFilter(self)
        self.setMinimumSize(200, 60)
        self._duration = duration
        self._isClosable = isClosable
        self._toastColor = toastColor
        self._position = position
        self.__isCustomBgcColor = isCustomBgcColor
        self.__bgcColor = QColor(bgcColor) if isCustomBgcColor else None

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.vBoxLayout = VBoxLayout(self)
        self.hBoxLayout = HBoxLayout()
        self.hBoxLayout.setSpacing(50)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.title = SubtitleLabel(title, self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.content = BodyLabel(content, self)

        self.initLayout()
        self.manager = ToastInfoBarManager.get(self._position)

    def initLayout(self):
        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setVisible(self._isClosable)
        self.closeButton.clicked.connect(self.__createOpacityAni)

        self.hBoxLayout.addWidget(self.title, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.closeButton, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.vBoxLayout.addWidget(self.content)

    def adjustSize(self):
        super().adjustSize()
        self.closeButton.adjustSize()

    def getBgcColor(self):
        if not self.__isCustomBgcColor:
            self.__bgcColor = QColor('#202020') if isDarkTheme() else QColor('#ECECEC')
        return self.__bgcColor

    def setBgcColor(self, color: QColor | str):
        self.__bgcColor = QColor(color)

    def __createPosAni(self):
        self.__posAni = QPropertyAnimation(self, b'pos')
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self.startPosition)
        self.__posAni.setEndValue(self.endPosition)
        self.__posAni.start()
        self.__posAni.finished.connect(self.__posAni.deleteLater)

    def __createOpacityAni(self):
        self.__opacityAni = QPropertyAnimation(self.opacityEffect, b'opacity')
        self.__opacityAni.setDuration(300)
        self.__opacityAni.setStartValue(1)
        self.__opacityAni.setEndValue(0)
        self.__opacityAni.start()
        self.__opacityAni.finished.connect(lambda: (self.hide(), self.__opacityAni.deleteLater()))

    @classmethod
    def new(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            toastColor: Union[QColor, str, ToastInfoBarColor] = ToastInfoBarColor.SUCCESS,
            isCustomBgcColor=False,
            bgcColor: QColor | str = None
    ):
        ToastInfoBar(
            parent, title, content, duration, isClosable,
            position, QColor(toastColor), isCustomBgcColor, bgcColor
        ).show()

    @classmethod
    def success(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.SUCCESS.value)

    @classmethod
    def error(
            cls, parent: QWidget, title: str, content: str,
            duration=-1, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.ERROR.value)

    @classmethod
    def warning(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.WARNING.value)

    @classmethod
    def info(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.INFO.value)

    @classmethod
    def custom(
            cls, parent: QWidget, title: str, content: str, toastColor: QColor | str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT,
            isCustomBgcColor=False, bgcColor: QColor | str = None
    ):
        cls.new(parent, title, content, duration, isClosable, position, toastColor, isCustomBgcColor, bgcColor)

    def showEvent(self, event):
        super().showEvent(event)
        self.manager.add(self)
        self.startPosition, self.endPosition = self.manager.getPos(self)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.closeSignal.emit()
        self.deleteLater()

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.move(self.manager.getPos(self)[1])
        return super().eventFilter(obj, event)

    def show(self):
        self.setVisible(True)
        self.__createPosAni()
        QTimer.singleShot(self._duration, self.__createOpacityAni)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._toastColor)
        painter.drawRoundedRect(0, 0, self.width() - 0.1, self.height(), 8, 8)

        painter.setBrush(self.getBgcColor())
        painter.drawRoundedRect(0, 5, self.width(), self.height() - 5, 6, 6)


class ToastInfoBarManager(QObject):
    """ ToastInfoBar manager """
    _instance = None
    registry = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToastInfoBarManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.margin = 24
        self.infoBars = []
        self.__initialized = True

    def add(self, infoBar: ToastInfoBar):
        infoBar.closeSignal.connect(lambda: self.remove(infoBar))
        self.infoBars.append(infoBar)

    def remove(self, infoBar: ToastInfoBar):
        self.infoBars.remove(infoBar)
        self.__adjustMove()

    def __adjustMove(self):
        for bar in self.infoBars:
            bar.move(self.getPos(bar)[1])

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType

        return decorator

    @classmethod
    def get(cls, operation):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation]()

    def getPos(self, infoBar: ToastInfoBar):
        raise NotImplementedError


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP)
class TopToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width()) / 2
        y = -infoBar.height() + self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y), QPoint(x, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_LEFT)
class TopLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        infoBar.adjustSize()
        y = -self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(-infoBar.width(), y), QPoint(self.margin, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_RIGHT)
class TopRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        infoX = infoBar.width()
        y = -self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(x + infoX, y), QPoint(x - infoX - self.margin, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM)
class BottomToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width()) / 2
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y), QPoint(x, y - infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_LEFT)
class BottomLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(-infoBar.width(), y), QPoint(self.margin, y - infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_RIGHT)
class BottomRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x + self.margin, y), QPoint(x - infoBar.width() - self.margin, y - infoBar.height())