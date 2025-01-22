# coding:utf-8
from PySide6.QtGui import QColor, QImage


if __name__ == '__main__':
    color = 'red'
    print(type(color))

    color = QColor(color)
    print(type(color), color.name())

    color = QColor(color)
    print(type(color), color.name())

    image = QImage('C:\\')
    print(type(image))

    image = QImage(image)
    print(type(image))