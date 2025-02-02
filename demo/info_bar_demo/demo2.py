import sys

from FluentWidgets import Widget, VBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from qfluentwidgets import InfoBar, PushButton


class Window(Widget):
    def __init__(self):
        super().__init__()
        print(QColor(None) is None)
        self.layout = VBoxLayout(self)
        self.btn = PushButton('show info bar', self)

        self.layout.addWidget(self.btn)

        self.btn.clicked.connect(lambda: InfoBar.success(
            'title', 'content', parent=self
        ))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())