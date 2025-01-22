# coding:utf-8

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPainter, Qt, QPainterPath, QImage
from PySide6.QtWidgets import  QWidget
from qfluentwidgets import isDarkTheme, Theme, setTheme


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self._xRadius = 0
        self._yRadius = 0
        self._opacity = 1.0
        self._backgroundImg = None # type: QImage | str
        self._darkColor = QColor(32, 32, 32)
        self._lightColor = QColor(243, 243, 243)

    def setBackgroundImg(self, image: QImage | str = None):
        """ set background image """
        self._backgroundImg = QImage(image)
        self.update()

    def setOpacity(self, opacity: float):
        """ set background opacity, range from 0 to 1 """
        self.setWindowOpacity(opacity)

    def setRadius(self, xRadius: int, yRadius: int):
        """ set widget radius """
        self._xRadius = xRadius
        self._yRadius = yRadius
        self.update()

    def setDarkColor(self, color: QColor | str):
        self._darkColor = QColor(color)
        self.update()

    def setLightColor(self, color: QColor | str):
        self._lightColor = QColor(color)
        self.update()

    def setBackgroundColor(self, light: QColor, dark: QColor):
        self.setDarkColor(dark)
        self.setLightColor(light)

    def getColor(self):
        return self._darkColor if isDarkTheme() else self._lightColor

    def getXRadius(self):
        return self._xRadius

    def getYRadius(self):
        return self._yRadius

    def getBackgroundImg(self):
        return self._backgroundImg

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform)
        painter.setBrush(self.getColor())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())
        if self._backgroundImg is not None:
            path = QPainterPath()
            rect = QRectF(self.rect())
            path.addRoundedRect(rect, self.getXRadius(), self.getYRadius())
            painter.setClipPath(path)
            painter.drawImage(rect, self.getBackgroundImg())