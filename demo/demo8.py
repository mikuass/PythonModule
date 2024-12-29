from FluentWidgets import VerticalScrollWidget, LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, \
    BottomPopDrawerWidget, DragFileWidget, DragFolderWidget, ComboBoxCard, SmoothScrollWidget
from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import QApplication
from qfluentwidgets import PrimaryPushButton, setTheme, Theme, FluentIcon


class Window(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('frame')
        self.setWindowTitle("QFrame 动画示例")
        self.resize(800, 600)
        self.drawerWidgets = []
        self.initWidget()
        self.connectSignalSlot()
        self.initVerticalScrollWidget()

    def initWidget(self):
        widgets = {
            '弹出左侧抽屉': {
                'widget': LeftPopDrawerWidget,
                'duration': 350,
                'width': 300,
                'height': self.height()
            },
            '弹出右侧抽屉': {
                'widget': RightPopDrawerWidget,
                'duration': 450,
                'width': 540,
                'height': self.height()
            },
            '弹出顶部抽屉': {
                'widget': TopPopDrawerWidget,
                'duration': 350,
                'width': self.width(),
                'height': 250
            },
            '弹出底部抽屉': {
                'widget': BottomPopDrawerWidget,
                'duration': 350,
                'width': self.width(),
                'height': 250
            },
        }
        for key, value in widgets.items():
            button = PrimaryPushButton(key, self)
            # drawer = value['widget'](self, width=value['width'], height=value['height'])
            drawer = value['widget'](self, key, QEasingCurve.Type.InBack, value['duration'], value['width'], value['height'])
            self.vBoxLayout.addWidget(button)
            button.clicked.connect(drawer.showDrawer)
            self.drawerWidgets.append(drawer)

        self.dragFile = DragFileWidget(self)
        self.dragFolder = DragFolderWidget(self)
        self.drawerWidgets[0].addWidget(self.dragFile)
        self.drawerWidgets[0].addWidget(self.dragFolder)

    def initVerticalScrollWidget(self):
        self.vScrollWidget = SmoothScrollWidget(self)
        self.vScrollWidget.vBoxLayout = self.vScrollWidget.createVBoxLayout()
        self.drawerWidgets[1].addWidget(self.vScrollWidget)
        for _ in range(24):
            comboBoxCard = ComboBoxCard(
                FluentIcon.HOME,
                '标题',
                '内容',
                ['item1', 'item2', 'item3', 'item4', 'item5']
            )
            comboBoxCard.setFixedWidth(500)
            comboBoxCard.comboBoxButton.currentIndexChanged.connect(lambda index: print(f'当前选中值下标: {index}'))
            self.vScrollWidget.vBoxLayout.addWidget(comboBoxCard)

    def connectSignalSlot(self):
        self.dragFile.draggedChange.connect(lambda filePath: print(f'文件拖入: {filePath}'))
        self.dragFile.selectionChange.connect(lambda filePath: print(f'选择了文件: {filePath}'))

        self.dragFolder.draggedChange.connect(lambda folderPath: print(f'文件夹拖入: {folderPath}'))
        self.dragFolder.selectionChange.connect(lambda folderPath: print(f'选择了文件夹: {folderPath}'))

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