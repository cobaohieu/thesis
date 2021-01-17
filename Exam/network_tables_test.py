#!/usr/bin/env python

import time
import threading

from networktables import NetworkTables
import logging

logging.basicConfig(level=logging.DEBUG)

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='10.11.65.2')

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

print("Connected!")
smart_dash = NetworkTables.getTable('SmartDashboard')

x0 = 15
x1 = 20
y0 = 35
y1 = 50

while True:
    smart_dash.putNumber('Pixy X0', x0)
    smart_dash.putNumber('Pixy Y0', y0)
    smart_dash.putNumber('Pixy X1', x1)
    smart_dash.putNumber('Pixy Y1', y1)

    smart_dash.putNumber('Pixy TimeStamp', int(time.time()))

    time.sleep (1)
