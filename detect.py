#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__      = "Hieu Bao Co"
__copyright__   = "Copyright 2020, kurokesu.com"
__version__ = "0.1"
__license__ = "GPL"

import sys
import usb
import usb.core
import usb.util
import usb.backend.libusb1
import cv2
import numpy as numpy
from time import gmtime, strftime
import time

VENDOR_ID = 0xb1ac
PRODUCT_ID = 0xf000
BDeviceClass = 255

print("Time",strftime("%Y-%m-%d %H:%M:%S", gmtime()))

devClass = usb.core.find(bDeviceClass=BDeviceClass)
printers = usb.core.find(find_all=True, bDeviceClass=BDeviceClass)

# SUBSYSTEM=="usb", ATTR{idVendor}=="1fc9", ATTR{idProduct}=="000c", MODE="0666"

# find our device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    # sys.exit("Could not find device")
    # sys.stdout.write("error: No Pixy devices have been detected.")
    raise RuntimeError('Pixy CMU5 camera device is not found.')
else:
    print ("Pixy CMU5 camera device is found!")

reattach = False

# was it found?
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)
    dev.reset()

print("deviceClass = " + str(dev.bDeviceClass))
for cfg in dev:
    sys.stdout.write("configuration: " + str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\tInterface: ' + \
                             str(intf.bInterfaceNumber) + \
                             ',' + \
                             str(intf.bAlternateSetting) + \
                             '\n')
        for ep in intf:
            sys.stdout.write('\t\tEndpoint: ' + \
                                  str(ep.bEndpointAddress) + \
                                  ',' + \
                                  str(ep.bmAttributes) + \
                                  '\n')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()


for bRequest in range(255):
    try:
        ret = dev.ctrl_transfer(0xC0, bRequest, 0, 0, 1)
        print("bRequest ",bRequest)
        print(ret)
    except:
        # failed to get data for this request
        pass

# ret = dev.ctrl_transfer(0x40, 0x6, 0x1, 0, [])
# print(ret)

# while True:
#     # Get data from brequest 0x32
#     ret = dev.ctrl_transfer(0xC0, 0x32, 0x0, 0x0, 10)
#     #print map(hex, ret)

#     x = (ret[2] << 8) | ret[3]
#     x = (x + 2 ** 15) % 2**16 - 2**15     # convert to signed 16b
#     y = (ret[4] << 8) | ret[5]
#     y = (y + 2 ** 15) % 2**16 - 2**15     # convert to signed 16b
#     z = (ret[6] << 8) | ret[7]
#     z = (z + 2 ** 15) % 2**16 - 2**15     # convert to signed 16b

#     print(x, "\t", y, "\t", z)

# first endpoint
endpoint = dev[0][(0,0)][0]



# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(dev,interface_number)
intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, bAlternateSetting = alternate_setting)
alt = usb.util.find_descriptor(cfg, find_all=True, bInterfaceNumber=1)


ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

if (ep is None):
    print("Success connect Pixy CMU5")
    # content for do something
    
else:
    print("error: No Pixy devices have been detected.")

