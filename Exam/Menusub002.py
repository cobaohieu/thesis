import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Example(QMainWindow):
    
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.setWindowIcon(QIcon('PixyControl-1.png'))
        
        self.initUI()

    def initUI(self):         
            
            menubar = self.menuBar()
            actionMenu = menubar.addMenu('Action')
            
            powerMenu = QMenu('Power', self)
            power_on = QAction('On', self) 
            powerMenu.addAction(power_on)
            power_off = QAction('Off', self) 
            powerMenu.addAction(power_off)

            recordMenu = QMenu('Record', self)
            record_play = QAction('Play', self)
            recordMenu.addAction(record_play)
            record_pause = QAction('Pause', self)
            recordMenu.addAction(record_pause)
                
            getFrame = QAction('Get Frame', self)

            actionMenu.addMenu(powerMenu)
            actionMenu.addMenu(recordMenu)
            actionMenu.addAction(getFrame)
            self.setGeometry(300, 300, 300, 200)
            self.setWindowTitle('Submenu')    
            self.show()
            
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())