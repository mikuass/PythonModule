# coding:utf-8
from PySide6.QtGui import QColor
from qfluentwidgets import Theme, themeColor, qconfig, setTheme


class BackgroundColor:
    def __init__(self, lightColor: QColor, darkColor: QColor):
        self.__lightColor = lightColor
        self.__darkColor = darkColor

    def getLightColor(self):
        return self.__lightColor

    def getDarkColor(self):
        return self.__darkColor


if __name__ == '__main__':
    qconfig.themeColorChanged.connect(lambda color: print(color))
    setTheme(Theme.DARK)
