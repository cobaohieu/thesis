import usb
import usb.core
import usb.util
import usb.backend.libusb1

dev = None
ep = None


dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_settting = usb.control.get_interface(dev,interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
    bAlternateSetting = 0
)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)

assert ep is not None

# write the data
ep.write('test')

