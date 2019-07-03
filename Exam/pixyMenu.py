import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class PixyControl(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Pixy Camera Control')
        self.setWindowIcon(QIcon('PixyControl-1.png'))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.statusBar().showMessage('This is a status bar')
        self.setGeometry(0, 0, 678, 626)
        self.resize(678, 626)

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
        self.initUI()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selected(self, q):
        print(q.text() + ' selected')

    def initUI(self):

        # self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) # only for Mac OS

        # 0 
        fileMenu = menubar.addMenu('File')
        actionMenu = menubar.addMenu('Action')
        helpMenu = menubar.addMenu('Help')

        configure_action = QAction('Configure', self)
        configure_action.setShortcut('Ctrl+,')

        saveImages_action = QAction('Save', self)
        saveImages_action.setShortcut('Ctrl+I')

        loadParameters_action = QAction('Load Parameters', self)
        loadParameters_action.setShortcut('Ctrl+L')

        saveParameters_action = QAction('Save Parameters', self)
        saveParameters_action.setShortcut('Ctrl+P')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+W')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.exitCall)

        # 2

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

        # 1
        fileMenu.addAction(configure_action)
        fileMenu.addAction(saveParameters_action)
        fileMenu.addAction(loadParameters_action)
        fileMenu.addAction(saveImages_action)
        fileMenu.addAction(exit_action)

        # 2
        actionMenu.addMenu(powerMenu)
        actionMenu.addMenu(recordMenu)
        actionMenu.addAction(getFrame_action)

        # 3
        helpMenu.addAction(help_action)
        helpMenu.addAction(about_action)

        # 4
        # quit_action.trigger.connect(self.quit_trigger)
        # fileMenu.trigger.connect(self.selected)


        # self = QWidget()

        # Color for text
        
       

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
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
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        # View Multi Text
        self.b = QPlainTextEdit(self)
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

    # def usbDetect():
        

    # def usbConnect():

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName))
            )
            self.playButton.setEnabled(True)

    def playCamera(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState: 
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # def pauseCamera():

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def postionChange(self, duration):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def exitCall(self):
        sys.exit(app.exec_())

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

def main():
    app = QApplication(sys.argv)
    print("input parameters = " + str(sys.argv))
    cbh = PixyControl()
    cbh.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()