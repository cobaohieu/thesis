import sys
import usb
import usb.core
import usb.util
import usb.backend.libusb1
import cv2
import numpy as numpy

devClass = usb.core.find(bDeviceClass=255)
if devClass is None:
    sys.stdout.write('error: No Pixy devices have been detected.')

# SUBSYSTEM=="usb", ATTR{idVendor}=="1fc9", ATTR{idProduct}=="000c", MODE="0666"


dev = usb.core.find(idVendor=0x1fc9, idProduct=0x000c)

if dev is None:
    sys.stdout.write("error: No Pixy devices have been detected.")

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
alt = usb.util.find_descriptor(cfg, find_all=True, bInterfaceNumber=1)

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT
)
# assert ep is not None, \
#        print("Success connect Pixy CMU5")
#
# ep.write('\x01')
if (ep is None):
    print("Success connect Pixy CMU5")
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc,20.0, (640,400))
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(frame)
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
else:
    print("error: No Pixy devices have been detected.")
# ep.write('test')

