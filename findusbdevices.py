import os
import usb
import usb.core
import usb.util
import usb.backend.libusb1


#find device
dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)
#found?
if dev is None :
        raise ValueError('device not found')

#set the active config. with no args, the first config will be the active one

dev.set_configuration()


#get an end point instance
ep = usb.util.find_descriptor(
    dev.get_interface_altsetting(), #first interface
    #match the first Out Endpoint
    custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)
assert ep is not None

while(1):
    ep.write('Success connect Pixy CMU')