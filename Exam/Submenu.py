# using python 3
# utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MenuPixy(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):        

        self.statusBar()

        # Create Menu Bar
        menubar = self.menuBar()

        # root menu
        fileMenu = menubar.addMenu('File')
        actionMenu = menubar.addMenu('Action')
        otherMenu = menubar.addMenu('Help')

        # Button Exit
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.setStatusTip('Exit application')
        # exit_action.triggered.connect(qApp.quit)

        # Button Save Images
        saveImages_action = QAction(QIcon('saveImages.png'), '&Save Images', self)
        saveImages_action.setShortcut('Ctrl+S')
        # saveImages_action.triggered.connect(qApp.saveImages)

        # Button Configure
        config_action = QAction(QIcon('config.png'), '&Configure', self)
        config_action.setShortcut('Ctrl+,')
        # config_action.triggered.connect(qApp.config)

        # Button Save Parameters Pixy
        saveParameters_action = QAction(QIcon('saveParameters.png'), '&Save Parameters', self)
        saveParameters_action.setShortcut('Ctrl+Alt+S')
        # saveParameters_action.triggered.connect(qApp.saveParameters)

        # Button Load Pixy
        loadParameters_action = QAction(QIcon('loadParameters.png'), '&Load Parameters', self)
        loadParameters_action.setShortcut('Ctrl+L')
        # loadParameters_action.triggered.connect(qApp.loadParameters)

        # Button Power On
        powerOn_action = QAction(QIcon('powerOn.png'), '&Power On', self)
        # help_action.setShortcut('Ctrl+S')

        # Button Power Off
        powerOff_action = QAction(QIcon('help.png'), '&Power Off', self)
        # help_action.setShortcut('Ctrl+S')

        # Button Play
        play_action = QAction(QIcon('play.png'), '&Play', self)
        # help_action.setShortcut('Ctrl+S')

        # Button Pause
        pause_action = QAction(QIcon('pause.png'), '&Pause', self)
        # help_action.setShortcut('Ctrl+S')

        # Button GetFrame
        getFrame_action = QAction(QIcon('getFrame.png'), '&Get Frame', self)
        # help_action.setShortcut('Ctrl+S')


        # Button Help
        help_action = QAction(QIcon('help.png'), '&Help...', self)
        # help_action.triggered.connect(qApp.help)

        # Button About
        about_action = QAction(QIcon('about.png'), '&About...', self)
        # about_action.triggered.connect(qApp.about)
        
        # Menu File short A-Z
        fileMenu.addAction(config_action)
        fileMenu.addAction(saveParameters_action)
        fileMenu.addAction(loadParameters_action)
        fileMenu.addAction(saveImages_action)
        fileMenu.addAction(exit_action)

        # Menu Root Action Menus short A-Z

        actionMenu = actionMenu('Power')
        actionMenu.addAction(powerOn_action)
        actionMenu.addAction(powerOff_action)

        actionMenu = actionMenu('Record')
        actionMenu.addAction(play_action)
        actionMenu.addAction(pause_action)
        actionMenu.addAction(getFrame_action)

        # Menu Help short A-Z
        otherMenu.addAction(help_action)
        otherMenu.addAction(about_action)

        #Events
        # quit_action.triggered.connect(self.quit_trigger)
        # fileMenu.triggered.connect(self.selected)

        self.setGeometry(0, 0, 678, 626)
        self.resize(678, 626)
        self.center()
        self.setWindowTitle('Pixy Control')
        self.show()

    def center(self):
        # geometry of the main windows
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of windows centering it
        self.move(qr.topLeft())

    # def quit_trigger(self):
    #     qApp.quit()

    def selected(self, q):
        print(q.text() + ' selected')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MenuPixy()
    sys.exit(app.exec_())