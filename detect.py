#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
__author__      = "Hieu Bao Co"
__copyright__   = "Copyright 2020, kurokesu.com"
__version__ = "0.1"
__license__ = "GPL"
"""

import sys
import time
import numpy
import usb
import usb.core
import usb.util
import usb.backend.libusb1

# VENDOR_ID = 0xb1ac
# PRODUCT_ID = 0xf000
# B_DEVICE_CLASS = 255

def detectUsb(VENDOR_ID, PRODUCT_ID, B_DEVICE_CLASS):
    devClass = usb.core.find(bDeviceClass = B_DEVICE_CLASS)
    printers = usb.core.find(find_all = True, bDeviceClass = B_DEVICE_CLASS)

    # sudo cp pixy.rules /etc/udev/rules.d/
    # pixy.rules content like this:
    # SUBSYSTEM=="usb", ATTR{idVendor}=="1fc9", ATTR{idProduct}=="000c", MODE="0666"
    # SUBSYSTEM=="usb", ATTR{idVendor}=="b1ac", ATTR{idProduct}=="f000", MODE="0666"
    # SUBSYSTEM=="video4linux", SUBSYSTEMS=="usb", ATTRS{idVendor}=="1fc9", ATTRS{idProduct}=="000c", NAME="video2"
    # SUBSYSTEM=="video4linux", SUBSYSTEMS=="usb", ATTRS{idVendor}=="b1ac", ATTRS{idProduct}=="f000", NAME="video3"

    dev = usb.core.find(idVendor = VENDOR_ID, idProduct = PRODUCT_ID)
    if dev is None:
        data = "Pixy CMU5 camera device is not found..."
    else:
        data = "Pixy CMU5 camera device is found!"
    return data

