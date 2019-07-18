import pyudev
import serial
import time
import fcntl

context = pyudev.Context()
monitor = Monitor.from_netlink()
# For USB devices
monitor.filter_by(susbsytem='usb')
# OR specifically for most USB serial devices
monitor.filter_by(susbystem='tty')
for action, device in monitor:
    vendor_id = device.get('ID_VENDOR_ID')
    # I know the devices I am looking for have a vendor ID of 'B1AC'
    if vendor_id in ['B1AC']:
        print('Detected {} for device with vendor ID {}').format(action, vendor_id)

def is_my_serial_device(device):
    return device.get('ID_VENDOR_ID') == 'B1AC' and device.get('ID_PRODUCT_ID') == 'F000'

for action, device in monitor:
    if is_my_serial_device(device):
        # Do something with the device
        if action == 'add':
            print('I just added my serial device')
        elif action == 'remove':
            print('I just removed my serial device')

my_serial_device = serial.Serial('/dev/ttyACM1')
while not my_serial_device.isOpen():
    # wait until the port has been properly opened
    my_serial_device.open()
    time.sleep(.1)

# Read the serial port until a newline character appears
print(my_serial_device.readline())