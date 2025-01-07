# coding:utf-8
# encoding:utf-8
import sys
from enum import Enum

from FluentWidgets import VBoxLayout, PopDrawerWidgetBase, HBoxLayout
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRect, QPoint, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QFrame
from PySide6.QtWidgets import QWidget
from qfluentwidgets import InfoBar, PrimaryPushButton, InfoBarPosition, TitleLabel, BodyLabel, TransparentToolButton, \
    FluentIcon, SubtitleLabel, setTheme, Theme, qconfig


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 500)
        self.vBoxLayout = VBoxLayout(self)
        self.texts = [
            'Click Me Show TopLeft Success',
            'Click Me Show TopRight Error',
            'Click Me Show Top Warning',
            'Click Me Show Bottom Info',
            'Click Me Show BottomLeft Info',
            'Click Me Show BottomRight Info',
        ]
        self.functions = [
            lambda: InfoView.success(
                self, 'success', 'topLeft', True,
                2000, 'tl'
            ),
            lambda: InfoView.error(
                self, 'error', 'topRight', True,
                3000, 'tr'
            ),
            lambda: InfoView.warning(
                self, 'warning', 'top', True,
                2000, 'top'
            ),
            lambda: InfoView.info(
                self, 'info', 'bottom', True,
                2000, 'bottom'
            ),lambda: InfoView.info(
                self, 'info', 'bottomLeft', True,
                2000, 'bl'
            ),lambda: InfoView.info(
                self, 'info', 'bottomRight', True,
                3000, 'br'
            ),
        ]
        for text, function in zip(self.texts, self.functions):
            button = PrimaryPushButton(text, self)
            self.vBoxLayout.addWidget(button)
            button.clicked.connect(function)


class InfoBarColor(Enum):
    SUCCESS = 'green'
    ERROR = 'red'
    WARNING = 'orange'
    INFO = 'blue'
    NOTE = 'pink'

    def __new__(cls, color):
        obj = object.__new__(cls)
        obj.color = QColor(color)  # 自定义 QColor 对象
        return obj

    @property
    def value(self):
        """返回 QColor 对象，而不是原始字符串"""
        return self.color


class InfoViewPosition(Enum):
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5


class InfoView(QFrame):
    def __init__(
            self,
            parent,
            title,
            content,
            isClosable,
            duration,
            position,
            topBackgroundColor=None,
            backgroundColor=None,
    ):
        super().__init__(parent)
        self.setFixedSize(256, 100)
        setTheme(Theme.AUTO)
        self.margin = 12
        self.topBackgroundColor = topBackgroundColor
        self.backgroundColor = backgroundColor
        self.title = title
        self.content = content
        self.duration = duration

        if position == 'top':
            self.startPosition, self.endPosition = (
                QPoint((parent.width() - self.width() / 1.3) / 2, -self.height()),
                QPoint((parent.width() - self.width() / 1.3) / 2, 24)
            )
        elif position == 'bottom':
            self.startPosition, self.endPosition = (
                QPoint((parent.width() - self.width() / 1.3) / 2, parent.height() + -self.height()),
                QPoint((parent.width() - self.width() / 1.3) / 2, parent.height() - self.height() - 24)
            )
        elif position == 'tl':
            self.startPosition, self.endPosition = (QPoint(-self.width(), 24), QPoint(24, 24))
        elif position == 'tr':
            self.startPosition, self.endPosition = (
                QPoint(parent.width() + self.width(), 24),
                QPoint(parent.width() - self.width() - 24, 24)
            )
        elif position == 'bl':
            self.startPosition, self.endPosition = (
                QPoint(-self.width(), parent.height() - self.height() - 24),
                QPoint(24, parent.height() - self.height() - 24)
            )
        elif position == 'br':
            self.startPosition, self.endPosition = (
                QPoint(parent.width() + self.width(), parent.height() - self.height() - 24),
                QPoint(parent.width() - self.width() - 24, parent.height() - self.height() - 24)
            )

        # self.setMinimumWidth(120)
        self.vBoxLayout = VBoxLayout(self)
        self.hBoxLayout = HBoxLayout(self)
        self.hBoxLayout.setSpacing(50)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.title = SubtitleLabel(self.title, self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.closeButton.setIconSize(QSize(15, 15))
        self.content = BodyLabel(self.content, self)

        self.hBoxLayout.addWidgets_(
            [self.title, self.closeButton,],
            alignment=[Qt.AlignmentFlag.AlignLeft, Qt.AlignmentFlag.AlignRight]
        )

        self.closeButton.clicked.connect(self.hide)
        self.closeButton.setVisible(isClosable)

        self.vBoxLayout.addWidget(self.content)

    def getBackgroundColor(self):
        self.backgroundColor = QColor('#202020') if qconfig.theme == Theme.DARK else QColor('#ECECEC')
        return self.backgroundColor

    def getTopBackgroundColor(self):
        return self.topBackgroundColor

    def setBackgroundColor(self, color: QColor):
        self.backgroundColor = color

    def __runAnimation(self):
        self.__geometryAni = QPropertyAnimation(self, b'pos')
        self.__geometryAni.setDuration(200)
        self.__geometryAni.setStartValue(self.startPosition)
        self.__geometryAni.setEndValue(self.endPosition)
        self.__geometryAni.start()

    @classmethod
    def new(
            cls,
            parent,
            title,
            content,
            isClosable,
            duration,
            position,
            topBackgroundColor,
            backgroundColor=None
    ):
        InfoView(
            parent, title, content, isClosable, duration,
            position, topBackgroundColor, backgroundColor
        ).show()

    @classmethod
    def success(cls, parent, title, content, isClosable, duration, position):
        cls.new(
            parent, title, content, isClosable, duration,
            position, InfoBarColor.SUCCESS.value
        )

    @classmethod
    def error(cls, parent, title, content, isClosable, duration, position):
        cls.new(
            parent, title, content, isClosable, duration,
            position, InfoBarColor.ERROR.value
        )

    @classmethod
    def warning(cls, parent, title, content, isClosable, duration, position):
        cls.new(
            parent, title, content, isClosable, duration,
            position, InfoBarColor.WARNING.value
        )

    @classmethod
    def info(cls, parent, title, content, isClosable, duration, position):
        cls.new(
            parent, title, content, isClosable, duration,
            position, InfoBarColor.INFO.value
        )

    @classmethod
    def custom(cls):
        pass

    def show(self):
        self.setVisible(True)
        self.__runAnimation()
        QTimer.singleShot(self.duration, self.hide)

    def paintEvent(self, event):
        super().paintEvent(event)
        topPainter = QPainter(self)
        topPainter.setRenderHint(QPainter.RenderHint.Antialiasing)
        topPainter.setPen(Qt.PenStyle.NoPen)
        topPainter.setBrush(self.getTopBackgroundColor())
        topPainter.drawRoundedRect(0, 0, self.width() - 0.1, self.height(), 8, 8)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(0, 5, self.width(), self.height() - 5, 6, 6)

    @classmethod
    def register(cls, INFO):
        return INFO


# @InfoView.register(InfoViewPosition.TOP)
# class TopInfoView(InfoView):
#     pass
#
#
# @InfoView.register(InfoViewPosition.TOP_LEFT)
# class TopLeftInfoView(InfoView):
#     pass
#
#
# @InfoView.register(InfoViewPosition.TOP_RIGHT)
# class TopRightInfoView(InfoView):
#     pass
#
#
# @InfoView.register(InfoViewPosition.BOTTOM)
# class BottomInfoView(InfoView):
#     pass
#
#
# @InfoView.register(InfoViewPosition.BOTTOM_LEFT)
# class BottomLeftInfoView(InfoView):
#     pass
#
#
# @InfoView.register(InfoViewPosition.BOTTOM_RIGHT)
# class BottomRightInfoView(InfoView):
#     pass


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())