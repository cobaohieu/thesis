import os
import usb
import usb.core
import usb.util
import usb.backend.libusb1

# def get_backend_libusb01():
#     libusb01_location = os.getcwd()

#     # load-library (ctypes.util.find_library) workaround: also search the current folder
#     is_current_folder_in_search_path = True
#     if None == usb.backend.libusb0.get_backend():
#         is_current_folder_in_search_path = libusb01_location in os.environ['PATH']
#         if not is_current_folder_in_search_path:
#             os.environ['PATH'] += os.pathsep + libusb01_location

#     backend = usb.backend.libusb0.get_backend()

#     if not is_current_folder_in_search_path:
#         os.environ['PATH'] = os.environ['PATH'].replace(os.pathsep + libusb01_location, "")

#     return backend

# print("System32 exists: %s" % os.path.exists("C:\\Windows\\System32"))
# print("libusb-1.0.dll exists: %s" % os.path.exists("C:\\Windows\\System32\\libusb-1.0.dll"))

# find our device
dev = usb.core.find(idVendor=0xb1ac, idProduct=0xf000)


# was it found?
if dev is None:
    raise ValueError('Device not found')

# if usb.core.find(bDeviceClass=255) is None:
#     raise ValueError('No camera found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
ep.write('test')