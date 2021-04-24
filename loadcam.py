#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
__author__      = "Hieu Bao Co"
__copyright__   = "Copyright 2020, kurokesu.com"
__version__ = "0.1"
__license__ = "GPL"
"""

import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import shutil
import threading
import datetime
import time

from pygame import camera

def capture_images(self) -> None:

    vendor_id = 0xb1ac
    product_id = 0xf000
    """
    Captures an image from each active camera.
    """
    self.logger.debug("Capturing images")

    # Get real or simulated camera paths
    if not self.simulate:
        camera_paths = usb.get_camera_paths(self.vendor_id, self.product_id)
    else:
        camera_paths = []
        for i in range(self.num_cameras):
            camera_paths.append("simulate_path")

    # Check correct number of camera paths
    num_detected = len(camera_paths)
    if num_detected != self.num_cameras:
        message = "Incorrect number of cameras detected, expected {}, detected {}".format(self.num_cameras, num_detected)
        message += ". Proceeding with capture anyway"
        self.logger.warning(message)

    # Capture an image from each active camera
    for index, camera_path in enumerate(camera_paths):
        # Get timestring in ISO8601 format
        timestring = datetime.datetime.utcnow().strftime("%Y-%m-%d-T%H:%M:%SZ")

        # Get filename for individual camera or camera instance in set
        if self.num_cameras == 1:
            filename = "{}_{}.png".format(timestring, self.name)
        else:
            filename = "{}_{}.{}.png".format(timestring, self.name, index + 1)

        # Create image path
        capture_image_path = self.capture_dir + filename
        final_image_path = self.directory + filename

        # Capture image
        self.capture_image_pygame(camera_path, capture_image_path)
        shutil.move(capture_image_path, final_image_path)


if __name__ == "__main__":
    capture_images(self)