#!/usr/bin/python

import sys
import usb.core
import usb.util
import time

streams="Scott's Sound Level Meter:i"


try:
	dev=usb.core.find(idVendor=0x64bd,idProduct=0x74e3)





	print(dev)

	#print dev.read(0x81, 8, 100)

	dev.detach_kernel_driver(0)

	usb.util.claim_interface(dev, 0)

	print(dev.ctrl_transfer(0x81,5,0,0))


	cfg = dev.get_active_configuration()
	intf = cfg[(0,0)]

	des = usb.util.find_descriptor(
		intf,
		custom_match = \
		lambda e: \
			usb.util.endpoint_direction(e.bEndpointAddress) == \
			usb.util.ENDPOINT_IN)

	#print des


	assert dev is not None

	#print dev

	#print hex(dev.idVendor)+','+hex(dev.idProduct)

	#while True:
    	#time.sleep(1)
    	#ret = dev.ctrl_transfer(0x81,5,0,0,0x7)
    	#print ret
    	# dB = (ret[0]+((ret[1]&3)*256))*0.1+30
    	# print dB
    	# msg="{'dB':'"+str(dB)+"'}" 

except Exception as e: 
	print(e.stacktrace())
	usb.util.dispose_resources(dev)
	dev.reset()