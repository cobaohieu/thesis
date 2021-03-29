import usb
import usb.core
import usb.util
import usb.backend.libusb1
import sys

dev = None
ep = None

def findDevices():
    dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)
    if dev is None:
        raise ValueError('Our device is not connected')
    dev.set_configuration()
    cfg = dev.get_active_configuration()
    interface_number = cfg[(0,0)].bInterfaceNumber
    alternate_settting = usb.control.get_interface(dev, interface_number)
    intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, bAlternateSetting = 0)
    ep = usb.util.find_descriptor(
    intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT
    )
    assert ep is not None
    ep.write('test')
    return;

(dev, ep) = findDevices()