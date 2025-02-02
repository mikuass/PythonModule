import sys

from FluentWidgets import Widget, VBoxLayout, ToastInfoBarPosition, ToastInfoBar
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from qfluentwidgets import PushButton, InfoBar, Theme, setTheme


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.layout = VBoxLayout(self)

        self.tb = PushButton('top info bar', self)
        self.tlb = PushButton('top left info bar', self)
        self.trb = PushButton('top right info bar', self)

        self.bb = PushButton('bottom info bar', self)
        self.blb = PushButton('bottom left info bar', self)
        self.brb = PushButton('bottom right info bar', self)

        self.layout.addWidgets([
            self.tb,
            self.tlb,
            self.trb,
            self.bb,
            self.blb,
            self.brb
        ])

        self.connectSignalSlot()


    def connectSignalSlot(self):
        self.tb.clicked.connect(
            lambda:
            ToastInfoBar.success(
                self,
                'top',
                'success info bar'
                'success info bar'
                'success info bar'
                'success info bar'
                'success info bar\n'
                'success info bar'
                'success info bar'
                'success info bar'
                'success info bar'
                'success info bar\n'
                'success info bar\n'
                'success info bar\n'
                'success info bar\n',
                2000,
                True,
                ToastInfoBarPosition.TOP
            )
        )
        self.tlb.clicked.connect(
            lambda:
            ToastInfoBar.warning(
                self, 'top left', 'warning info bar', position=ToastInfoBarPosition.TOP_LEFT
            )
        )
        self.trb.clicked.connect(
            lambda:
            ToastInfoBar.info(
                self, 'top right', 'info bar', position=ToastInfoBarPosition.TOP_RIGHT
            )
        )
        self.bb.clicked.connect(
            lambda:
            ToastInfoBar.error(
                self, 'bottom', 'error info bar', position=ToastInfoBarPosition.BOTTOM
            )
        )
        self.blb.clicked.connect(
            lambda:
            ToastInfoBar.custom(
                self, 'bottom left', 'custom info bar', QColor('skyblue'), position=ToastInfoBarPosition.BOTTOM_LEFT
            )
        )
        self.brb.clicked.connect(
            lambda:
            ToastInfoBar.custom(
                self, 'bottom right', 'custom info bar', QColor('deeppink'), position=ToastInfoBarPosition.BOTTOM_RIGHT,
                isCustomBgcColor=True, bgcColor='deepskyblue'
            )
        )


    def resizeEvent(self, event):
        super().resizeEvent(event)
        print('Resize')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    setTheme(Theme.DARK)
    window.show()
    sys.exit(app.exec())