from FluentWidgets import VerticalScrollWidget, LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, \
    BottomPopDrawerWidget
from PySide6.QtWidgets import QApplication
from qfluentwidgets import PrimaryPushButton, setTheme, Theme


class Window(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('frame')
        self.setWindowTitle("QFrame 动画示例")
        self.resize(850, 600)
        self.drawerWidgets = []
        self.initWidget()
        self.connectSignalSlot()

    def initWidget(self):
        widgets = [LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, BottomPopDrawerWidget]
        for widget in widgets:
            drawer = widget(self)
            button = PrimaryPushButton(f'Show Drawer', drawer)
            button.clicked.connect(drawer.showDrawer)
            self.vBoxLayout.addWidget(button)
            self.drawerWidgets.append(drawer)

    def connectSignalSlot(self):
        pass

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        for drawer in self.drawerWidgets:
            drawer.hideDrawer()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for drawer in self.drawerWidgets:
            drawer.resizeEvent(event)
            drawer.hideDrawer()


if __name__ == '__main__':
    app = QApplication([])
    main_window = Window()
    setTheme(Theme.AUTO)
    main_window.show()
    app.exec()