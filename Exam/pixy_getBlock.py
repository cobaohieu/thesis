from microbit import *

class Pixy:
	def __init__(self, interface):
		self.interface = interface

		self.start_word = 0xaa55
		self.start_word_cc = 0xaa56
		self.start_word_x = 0x55aa
		self.max_signature_count = 7
		self.default_arg_val = 0xFFFF
		self.skip_start = False

		self.position_min_x = 0
		self.position_max_x = 319
		self.position_min_y = 0
		self.position_max_y = 199

		self.servo_min = 0
		self.servo_max = 1000
		self.servo_center = (self.servo_max - self.servo_min) / 2

	def get_blocks(, max_blocks = 100):

	def set_servos(self, servo_0, servo_1):
		__value_in_range(servo_0, 0, 1000)
		__value_in_range(servo_1, 0, 1000)
		buf = []
		buf[0], buff[1] = struct.unpack('>BB', servo_0)
		buf[2], buff[3] = struct.unpack('>BB', servo_1)
		interface.send(buf)


	def set_brightness(self, brightness):
		__value_in_range(brightness, 0, 255)
		interface.send([0x00, 0xFE, r, g, b])

	def set_led(self, r, g, b):
		for v in [r, g, b]:
			__value_in_range(v, 0, 255)
		interface.send([0x00, 0xFD, r, g, b])

	def __get_start(self):
		last_word = 0xFFFF
		while True:
			# todo: add some kind of timeout
			word = interface.get_word()
			if word == 0 and last_word == 0:
				return False
			elif (word == self.start_word) and (last_word == self.start_word):
				return True
			elif (word == self.start_word_cc) and (last_word == self.start_word):
				return True
			elif (word == self.start_word_x):
				interface.get_byte()
			last_word = word

	def __value_in_range(self, value, minimum, maximum):
		if value > maximum:
			raise ValueError('Value is too large (over {})'.format(maximum))
		elif value < minimum:
			raise ValueError('Value is too small (under {})'.format(minimum))

class PixyI2C:
	def __init__(self, pin_sda, pin_scl, address = 0x54):
		self.pin_sda = pin_sda
		self.pin_scl = pin_scl
		self.address = address

		i2c.init(freq = 100000, sda = self.pin_sda, scl = pin_scl)

	def get_word(self):
		# todo: request from
		data = i2c.read(self.address, 2)
		word = data[1] << 8
		word |= data[0]
		return word

	def get_byte(self):
		# todo: request from
		return i2c.read(self.address, 1)

	def send(self, data):
		i2c.write(self.address, bytes(data))