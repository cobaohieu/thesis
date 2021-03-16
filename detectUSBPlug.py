#!/usr/bin/python3

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
    raise RuntimeError('Pixy CMU5 camera device is not connected.')
else:
    print ("Pixy CMU5 camera device is connected!")

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
    # data = dev.read(0x83,3*640*480,100)

    # read a data packet
    data = None
    while True:
        try:
            data = dev.read(endpoint.bEndpointAddress,
                                endpoint.wMaxPacketSize)
            print("data")

        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):

                continue

else:
    print("error: No Pixy devices have been detected.")

