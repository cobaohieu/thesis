import sys
import usb
import usb.core

# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
  sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + ' & DeviceClass=' + str(cfg.bDeviceClass) + '\n')
  sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + ' & DeviceClass=' + hex(cfg.bDeviceClass) + '\n\n')