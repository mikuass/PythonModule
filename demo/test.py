# coding:utf-8
import sys
from enum import Enum

from PySide6.QtWidgets import QApplication, QStackedWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Qt
from FluentWidgets import Widget, HBoxLayout, NavigationBar, VBoxLayout
from qfluentwidgets import PrimaryPushButton, FluentIcon, TitleLabel, PopUpAniStackedWidget


class SubWidget(Widget):
    def __init__(self, parent=None, title=None):
        super().__init__(parent)
        self.layout = VBoxLayout(self)
        self.layout.addWidget(TitleLabel(title, self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(PrimaryPushButton(title, self))
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)


class Window(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = HBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget = PopUpStackedWidget()
        self.nav = NavigationBar(self)

        self.layout.addWidgets([self.nav, self.stackedWidget])

        self.w1 = SubWidget(self, 'interface1')
        self.w2 = SubWidget(self, 'interface2')
        self.w3 = SubWidget(self, 'interface3')
        self.w4 = SubWidget(self, 'interface4')
        self.w5 = SubWidget(self, 'interface5')
        self.stackedWidget.addWidget(self.w1)
        self.stackedWidget.addWidget(self.w2)
        self.stackedWidget.addWidget(self.w3)
        self.stackedWidget.addWidget(self.w4)
        self.stackedWidget.addWidget(self.w5)

        self.nav.addItem(
            'item1', FluentIcon.HOME, 'item1', True,
            lambda: self.stackedWidget.setCurrentWidget(self.w1)
        )
        self.nav.addItem(
            'item2', FluentIcon.HOME, 'item2', False,
            lambda: self.stackedWidget.setCurrentWidget(self.w2)
        )
        self.nav.addItem(
            'item3', FluentIcon.HOME, 'item3', False,
            lambda: self.stackedWidget.setCurrentIndex(2)
        )
        self.nav.addItem(
            'item4', FluentIcon.HOME, 'item4', False,
            lambda: self.stackedWidget.setCurrentWidget(self.w4)
        )
        self.nav.addItem(
            'item5', FluentIcon.HOME, 'item5', False,
            lambda: self.stackedWidget.setCurrentWidget(self.w5)
        )
        self.nav.enableReturn(True)
        self.nav.setCurrentItem('item1')
        # self.stackedWidget.setPopUpPosition(StackedPopUpPosition.CUSTOM_POSITION)(QPoint(0, self.height()), QPoint(0, 0))
        self.stackedWidget.setPopUpPosition(StackedPopUpPosition.BOTTOM_TO_TOP)


class StackedPopUpPosition(Enum):
    BOTTOM_TO_TOP = 0
    TOP_TO_BOTTOM = 1
    LEFT_TO_RIGHT = 2
    RIGHT_TO_LEFT = 3
    CUSTOM_POSITION = 4


class PopUpStackedWidget(QStackedWidget):
    def __init__(
            self,
            ease=QEasingCurve.Type.Linear,
            position=StackedPopUpPosition.BOTTOM_TO_TOP,
            duration=250,
            parent=None
    ):
        super().__init__(parent)
        self.__ani = None # type: QPropertyAnimation
        self._aniEase = ease
        self._duration = duration
        self.__startValue = None # type: QPoint
        self.__endValue = QPoint(0, 0) # type: QPoint
        self.setPopUpPosition(position)

    def setPopUpPosition(self, position: StackedPopUpPosition) -> any:
        """ position is CUSTOM_POSITION, return setPos function """
        if position == StackedPopUpPosition.CUSTOM_POSITION:
            return self.__setPos
        if position == StackedPopUpPosition.BOTTOM_TO_TOP:
            self.__startValue = QPoint(0, 100)
        elif position == StackedPopUpPosition.TOP_TO_BOTTOM:
            self.__startValue = QPoint(0, -100)
        elif position == StackedPopUpPosition.LEFT_TO_RIGHT:
            self.__startValue = QPoint(-100, 0)
        elif position == StackedPopUpPosition.RIGHT_TO_LEFT:
            self.__startValue = QPoint(100, 0)

    def setDuration(self, duration: int):
        self._duration = duration

    def __setPos(self, startValue: QPoint, endValue: QPoint):
        self.__startValue = startValue
        self.__endValue = endValue

    def setCurrentIndex(self, index):
        w = self.widget(index)
        self.setCurrentWidget(w)

    def setCurrentWidget(self, w):
        self.__createAni(w)
        super().setCurrentWidget(w)

    def __createAni(self, w):
        if self.currentIndex() == self.indexOf(w):
            return
        self.__currentIndex = self.indexOf(w)
        self.__ani = QPropertyAnimation(w, b'pos')
        self.__ani.setDuration(self._duration)
        self.__ani.setEasingCurve(self._aniEase)
        self.__ani.setStartValue(self.__startValue)
        self.__ani.setEndValue(self.__endValue)
        self.__ani.finished.connect(self.__ani.deleteLater)
        self.__ani.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())