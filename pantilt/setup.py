#!/usr/bin/python3

from distutils.core import setup, Extension

# The paths used in this file are relative to: PIXY_ROOT/build #

pixy_module = Extension('_pixy',
	include_dirs = ['/usr/include/libusb-1.0',
  '/usr/local/include/libusb-1.0',
	'../../common/inc',
	'../../libpixyusb/',
  '../../libpixyusb/include'],
	libraries = ['boost_thread',
	'boost_system',
	'boost_chrono',
	'pthread',
	'usb-1.0'],
	sources=['pixy_wrap.cxx',
	'../../common/chirp.cpp',
	'../../libpixyusb/pixy.cpp',
	'../../libpixyusb/chirpreceiver.cpp',
	'../../libpixyusb/pixyinterpreter.cpp',
	'../../libpixyusb/usblink.cpp',
	'../../libpixyusb/timer.cpp'])

setup (name = 'pixy',
	version = '0.3',
	author  = 'Charmed Labs, LLC',
	description = """libpixyusb module""",
	ext_modules = [pixy_module],
	py_modules = ["pixy"],
	)
