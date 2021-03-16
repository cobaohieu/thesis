#!/usr/bin/env python
""" shrek_vision.py - team 1165 pixycam

Take pixycam vector structure and put values into NetworkTables on rio.

"""

import time
import pixy
from ctypes import *
from pixy import *
from networktables import NetworkTables
import logging


class Vector (Structure):
    _fields_ = [
      ("m_x0", c_uint),
      ("m_y0", c_uint),
      ("m_x1", c_uint),
      ("m_y1", c_uint),
      ("m_index", c_uint),
      ("m_flags", c_uint) ]

class IntersectionLine (Structure):
    _fields_ = [
      ("m_index", c_uint),
      ("m_reserved", c_uint),
      ("m_angle", c_uint) ]

def main():

    # Initialize the pixycam and select the line following program.
    pixy.init ()
    pixy.change_prog ("line")

    # NetworkTables requires logging module
    logging.basicConfig(level=logging.DEBUG)

    # Connect to network tables server on the IP address of the Rio.
    NetworkTables.initialize(server='10.11.65.2')

    # Connect to SmartDashboard
    smart_dash = NetworkTables.getTable('SmartDashboard')

    # Initialize a Vector Object with a (very generous) 10 slots
    # (We ever only want to pay attention to the first vector anyway.)

    vectors = VectorArray(10)

    # loop forever.  Not very pythonic, but it's what we need.
    while True:
        # get all of the current features (what the pixycam sees)
        line_get_all_features ()

        # fetch the top 10 vectors from pixy
        vector_count = line_get_vectors (10, vectors)

        # If there are any vectors, v_count will be greater than zero.
        if vector_count > 0:
            smart_dash.putNumber('Pixy X0', vectors[0].m_x0 )
            smart_dash.putNumber('Pixy Y0', vectors[0].m_y0 )
            smart_dash.putNumber('Pixy X1', vectors[0].m_x1 )
            smart_dash.putNumber('Pixy Y1', vectors[0].m_y1 )
    time.sleep(1)

## End of main()

if __name__ == "__main__":
    main()
