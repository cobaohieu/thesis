#!/usr/bin/env python
import sys
import requests
import json
import websocket
import time
import usb
import usb.core
import usb.util
import usb.backend.libusb1

dev = None
ep = None


def connect_to_scanner():
    # find our zebra device
    dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)

    # was it found ?
    if dev is None:
        print("Device not found (meaning it is disconnected)")
        return (None, None)

    # detach the kernel driver so we can use interface (one user per interface)
    reattach = False
    print(dev.is_kernel_driver_active(0))
    if dev.is_kernel_driver_active(0):
        print("Detaching kernel driver")
        reattach = True
        dev.detach_kernel_driver(0)

    # set the active configuration; with no arguments, the first configuration
    # will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    interface_number = cfg[(0, 0)].bInterfaceNumber
    alternate_setting = usb.control.get_interface(dev, interface_number)
    intf = usb.util.find_descriptor(
        cfg, bInterfaceNumber=interface_number,bAlternateSetting=alternate_setting
    )

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

    assert ep is not None
    ep.write('Success connect Pixy CMU')
    return (dev, ep)

(dev, ep) = connect_to_scanner()
