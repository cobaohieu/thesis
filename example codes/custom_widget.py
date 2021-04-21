#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

In this example, we create a custom widget.

Author: Jan Bodnar
Website: zetcode.com
"""

from PyQt5.QtWidgets import (QWidget, QSlider, QApplication,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
import sys


class Communicate(QObject):
    updateBW = pyqtSignal(int)


class RedSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(0, 30)
        self.value = 0
        self.num = [55, 105, 155, 205, 255]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        MAX_CAPACITY = 255
        OVER_CAPACITY = 306

        font = QFont('Google Sans', 10, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 6))

        till = int(((w / OVER_CAPACITY) * self.value))
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))

        if self.value >= MAX_CAPACITY:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(176, 0, 32))

            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till - full, h)

        else:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(176, 0, 32))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        for i in range(step, 6 * step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))

            x, y = int(i - fw/2), int(h / 2)
            qp.drawText(x, y, str(self.num[j]))
            j = j + 1


class GreenSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(0, 30)
        self.value = 0
        self.num = [55, 105, 155, 205, 255]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        MAX_CAPACITY = 255
        OVER_CAPACITY = 306

        font = QFont('Google Sans', 10, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 6))

        till = int(((w / OVER_CAPACITY) * self.value))
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))

        if self.value >= MAX_CAPACITY:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(1, 135, 134))

            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till - full, h)

        else:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(1, 135, 134))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        for i in range(step, 6 * step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))

            x, y = int(i - fw/2), int(h / 2)
            qp.drawText(x, y, str(self.num[j]))
            j = j + 1

class BlueSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(0, 30)
        self.value = 0
        self.num = [55, 105, 155, 205, 255]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        MAX_CAPACITY = 255
        OVER_CAPACITY = 306

        font = QFont('Google Sans', 10, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 6))

        till = int(((w / OVER_CAPACITY) * self.value))
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))

        if self.value >= MAX_CAPACITY:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(3, 54, 255))

            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till - full, h)

        else:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(3, 54, 255))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        for i in range(step, 6 * step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))

            x, y = int(i - fw/2), int(h / 2)
            qp.drawText(x, y, str(self.num[j]))
            j = j + 1

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        OVER_CAPACITY = 255

        #red
        horizontalSlider_red = QSlider(Qt.Horizontal, self)
        horizontalSlider_red.setFocusPolicy(Qt.NoFocus)
        horizontalSlider_red.setRange(1, OVER_CAPACITY)
        horizontalSlider_red.setValue(0)
        horizontalSlider_red.setGeometry(50, 14, 255, 13)

        #green
        horizontalSlider_green = QSlider(Qt.Horizontal, self)
        horizontalSlider_green.setFocusPolicy(Qt.NoFocus)
        horizontalSlider_green.setRange(1, OVER_CAPACITY)
        horizontalSlider_green.setValue(0)
        horizontalSlider_green.setGeometry(50, 46, 255, 13)

        #blue
        horizontalSlider_blue = QSlider(Qt.Horizontal, self)
        horizontalSlider_blue.setFocusPolicy(Qt.NoFocus)
        horizontalSlider_blue.setRange(1, OVER_CAPACITY)
        horizontalSlider_blue.setValue(0)
        horizontalSlider_blue.setGeometry(50, 77, 255, 13)

        self.c = Communicate()

        # red
        self.widred = RedSlider()
        self.c.updateBW[int].connect(self.widred.setValue)

        # green
        self.widgreen = GreenSlider()
        self.c.updateBW[int].connect(self.widgreen.setValue)

        # blue
        self.widblue = BlueSlider()
        self.c.updateBW[int].connect(self.widblue.setValue)

        # red
        horizontalSlider_red.valueChanged[int].connect(self.changeValueRed)
        hboxred = QHBoxLayout()
        hboxred.addWidget(self.widred)

        # green
        horizontalSlider_green.valueChanged[int].connect(self.changeValueGreen)
        hboxgreen = QHBoxLayout()
        hboxgreen.addWidget(self.widgreen)

        # blue
        horizontalSlider_blue.valueChanged[int].connect(self.changeValueBlue)
        hboxblue = QHBoxLayout()
        hboxblue.addWidget(self.widblue)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hboxred)
        vbox.addLayout(hboxgreen)
        vbox.addLayout(hboxblue)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('Burning widget')
        self.show()

    def changeValueRed(self, value):
        self.c.updateBW.emit(value)
        self.widred.repaint()
        # self.widgreen.repaint()
        # self.widblue.repaint()

    def changeValueGreen(self, value):
        self.c.updateBW.emit(value)
        # self.widred.repaint()
        self.widgreen.repaint()
        # self.widblue.repaint()

    def changeValueBlue(self, value):
        self.c.updateBW.emit(value)
        # self.widred.repaint()
        # self.widgreen.repaint()
        self.widblue.repaint()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()