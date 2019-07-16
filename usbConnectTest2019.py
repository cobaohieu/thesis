import sys
import usb
import usb.core
import usb.util
import usb.backend.libusb1



devClass = usb.core.find(bDeviceClass=255)
if devClass is None:
    sys.stdout.write('error: No Pixy devices have been detected.')

dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)
if dev is None:
    sys.stdout.write("error: No Pixy devices have been detected.")

    # return;

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

dev.set_configuration()

cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_settting = usb.control.get_interface(dev,interface_number)
intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, bAlternateSetting = 0)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)
assert ep is not None, \
       print("Success connect Pixy CMU5")

# if (ep is not None):
#     print("Success connect Pixy CMU5")
# else:
#     print("error: No Pixy devices have been detected.")
# ep.write('test')

alt = usb.util.find_descriptor(cfg, find_all=True, bInterfaceNumber=1)