import sys
import usb
import usb.core
import usb.util
import usb.backend.libusb1

devClass = usb.core.find(bDeviceClass=255)
dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)

if devClass is None:
    raise ValueError('error: No Pixy devices have been detected.')

if dev is None:
    raise ValueError('error: No Pixy devices have been detected.')

dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None,  ep.write('Pixy detected.')
