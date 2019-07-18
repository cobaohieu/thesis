import os
import sys
import usb.core
import usb.backend.libusb1
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class PixyCMU5(QMainWindow):

    def __init__(self):                     #, parent=None):
        super(PixyCMU5, self).__init__()    #(parent)
        self.setWindowTitle('Pixy Camera Control')
        #scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon('imgs/logo.png'))#(scriptDir + os.path.sep + 'logo.png'))
        self.initUI()

    def initUI(self):

        palette = qApp.palette()
        palette.setColor(QPalette.Text, QColor(255, 0, 0))

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create configure action
        configure_action = QAction('Configure', self)
        configure_action.setShortcut('Ctrl+,')

        # Create save images action
        saveImages_action = QAction('Save', self)
        saveImages_action.setShortcut('Ctrl+I')

        # Create load parameters action
        loadParameters_action = QAction('Load Parameters', self)
        loadParameters_action.setShortcut('Ctrl+L')

        # Create save parameters action
        saveParameters_action = QAction('Save Parameters', self)
        saveParameters_action.setShortcut('Ctrl+P')

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        powerMenu = QMenu('Power', self)

        power_on = QAction('On', self)
        power_on.setShortcut('F1')
        powerMenu.addAction(power_on)

        power_off = QAction('Off', self) 
        power_off.setShortcut('F2')
        powerMenu.addAction(power_off)

        recordMenu = QMenu('Record', self)

        record_play = QAction('Play', self) 
        record_play.setShortcut('F3')      
        recordMenu.addAction(record_play)     
           
        record_pause = QAction('Pause', self)
        record_pause.setShortcut('F4')
        recordMenu.addAction(record_pause)

        getFrame_action = QAction('Get Frame', self)

        # 3
        help_action = QAction('Help', self)
        # help_action.setShortcut('Ctrl+H')

        about_action = QAction('About', self)
        # about_action.setShortcut('')

        # Create menu bar and add action
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False) # only for Mac OS
        fileMenu = menuBar.addMenu('&File')
        actionMenu = menuBar.addMenu('&Action')
        helpMenu = menuBar.addMenu('&Help')

        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(configure_action)
        fileMenu.addAction(saveParameters_action)
        fileMenu.addAction(loadParameters_action)
        fileMenu.addAction(saveImages_action)
        fileMenu.addAction(exitAction)

        # actionMenu.addAction(newAction)
        actionMenu.addMenu(powerMenu)
        actionMenu.addMenu(recordMenu)
        actionMenu.addAction(getFrame_action)

        #helpMenu.addAction(newAction)
        helpMenu.addAction(help_action)
        helpMenu.addAction(about_action)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(4, 0, 0, 120)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.b = QPlainTextEdit(self)
        self.b.setReadOnly(True)
        # self.b.insertPlaintText("")
        self.b.move(14, 485)
        self.b.resize(649, 108)

        # Text In View
        self.t = QTextCursor(self.b.document())
        self.t.insertText("error: No Pixy devices have been detected.")

        self.t.insertBlock()
        self.t.block().setVisible(False)
        print(self.b.document().toPlainText())
        
        self.center()    

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selected(self, q):
        print(q.text() + ' selected')    

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        qApp.quit()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    # def usbDetect():
        

    # def usbConnect():


def main():
    app = QApplication(sys.argv)
    PixyControl = PixyCMU5()
    PixyControl.show()    
    PixyControl.resize(678, 626)
    PixyControl.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()