import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


app = QApplication([])

button = QPushButton('Click')
def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()

button.clicked.connect(on_button_clicked)
button.show()


# Ex2
#-------------------------------
# app.setStyle('Fusion')
# palette = QPalette()
# palette.setColor(QPalette.ButtonText, Qt.red)
# app.setPalette(palette)
# button = QPushButton('HelloWorld')
# button.show()

# Ex1
#-------------------------------
# window = QWidget()
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# window.show()

# Ex0
#-------------------------------
# label = QLabel('Hello World')
# label.show()

# Run app
app.exec_()