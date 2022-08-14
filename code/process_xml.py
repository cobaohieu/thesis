#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

import sys
import os
import datetime
import time
import numpy
import numpy as np
import usb
import usb.core
import usb.util
import usb.backend.libusb1
import csv
import ctypes
import cv2
import argparse
import imutils
import PyQt5
import logging
import xml.etree.ElementTree
import xml.etree.ElementTree as ET

from PyQt5 import QtGui
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse # , canonicalize
from xml.dom import minidom



sys.path.append(os.path.join(os.path.dirname(__file__), "./"))

file_name = 'config.xml'
# tree = parse(file_name)

# with open(file_name, mode='wb', encoding='utf-8') as f:
#     f.write(b_xml)

def readAllFields(fileName):
    tree = parse(file_name)
    root = tree.getroot()

    print("File:", file_name)
    print("Root:", root.tag)

    # print(root.attrib)

    # All item attributes
    # print('All attributes:')
    for child in root:
        print('Attribute:', child.tag, child.attrib) #, child.attrib)

    for config in root.findall('software'):
        image = config.find('image').text
        print(image)

    # all item attributes
    print('\nAll attributes .tag:')
    for elem in root:
        for subelem in elem:
            print(subelem.tag)

    # All items data
    print('\nAll value data .text:')
    for values in root:
        for subelem in values:
            print(subelem.text)

    for items,value in zip (root, root):
        if items.tag == 'brightness':
            print("\nbrightness:", value.text)

    for items,value in zip(root, root):
        item = items.get('name')
        if item == 'brightness':
            print("\nbrightness:",value.attrib)

    print('\nAll item data:')
    for type_tag in tree.findall('image/string'):
        value = type_tag.get('name')
        print("items:", value)

## Counting Document
def counting(fileName):
    tree = fileName
    root = tree.getroot()
    print(len(root[0]))

## Writing document
def writing(fileName):
    tree = fileName
    root = tree.getroot()
    data = Element('data')
    items = SubElement(data, 'item')
    item1 = SubElement(items, 'item')
    item2 = SubElement(items, 'item')
    item3 = SubElement(items, 'item')

    item1.set('name', 'item1')
    item2.set('name', 'item2')
    item3.set('name', 'item3')

    item1.text = 'item1abc'
    item2.text = 'item2abc'
    item3.text = 'item3abc'

    # Create a new XML file with the results
    mydata = tostring(data)
    myfile = open(fileName, "w")
    myfile.write(mydata)


## Finding
def finding(fileName):
    tree = fileName
    root = tree.getroot()
    # Find the first 'item' object
    for elem in root:
        print(elem.find('item').get('name'))

    # Find all "item" objects and print their "name" attribute
    for elem in root:
        for subelem in elem.findall('item'):
            # If we don't need to now the name of the attribute(s), get the dict
            print(subelem.attrib)

            # If we know the name of the attribute, access it directly
            print(subelem.get('name'))

    ## Modify
    # Changing a field text
    for elem in root.iter('item'):
        elem.text = 'new text'

    # modifying an attribute
    for elem in root.iter('item'):
        elem.set('name', 'newitem')

    # Adding an attribute
    for elem in root.iter('item'):
        elem.set('name2', 'newitem2')

    tree.write(fileName)

## Creating Sub-Elements
def create_sub_elements(fileName):
    tree = fileName
    root = tree.getroot()
    # Adding an element to the root node
    attrib = {}
    element = root.makeelement('seconditems', attrib)
    root.append(element)

    # Adding an element to the seconditem node
    attrib = {'name2': 'secondname2'}
    subelement = root[0][1].makeelement('seconditem', attrib)
    SubElement(root[1], 'seconditem', attrib)
    root[1][0].text = 'seconditemabc'

    # create a new xml file with the new element
    tree.write(fileName)

## Deleting
def delete(fileName):
    tree = fileName
    root = tree.getroot()
    # Deleting an atrribute
    # Removing an attribute
    root[0][1].attrib.pop('name', None)

    # create a new XML file with the results
    tree.write(fileName)

    # Deleting one sub-element
    # Removing one sub-element
    root[0].remove(root[0][0])

    # create a new XML file with the results
    tree.write(fileName)

    # Deleting all sub-elements
    # Removing all sub-elements of an element
    root[0].clear()

    # create a new XML file with the results
    tree.write(fileName)

## Reading file
def reading(fileName):
    tree = parse(file_name)
    root = tree.getroot()
    
    for elem in tree.getiterator():
        if elem.tag=='software':
            output={}
            for elem1 in list(elem):
                if elem1.tag=='name':
                    output['name']=elem1.text
            print(output)
    
    for elem in tree.getiterator():
        if elem.tag=='software':
            output={}
            for elem1 in list(elem):
                if elem1.tag=='version':
                    output['version']=elem1.text
            print(output)
    
    for elem in tree.getiterator():
        if elem.tag=='software':
            output={}
            for elem1 in list(elem):
                if elem1.tag=='copyright':
                    output['copyright']=elem1.text
            print(output)
    
    for elem in tree.getiterator():
        if elem.tag=='software':
            output={}
            for elem1 in list(elem):
                if elem1.tag=='year':
                    output['year']=elem1.text
            print(output)

    for elem in tree.getiterator():
        if elem.tag=='software':
            photo_config={}
            for elem1 in list(elem):
                if elem1.tag=='photo':
                    for elem2 in list(elem1):
                        if elem2.tag=='brightness':
                            photo_config['brightness']=elem2.text
                        if elem2.tag=='contrast':
                            photo_config['contrast']=elem2.text
                        if elem2.tag=='staturation':
                            photo_config['staturation']=elem2.text
                        if elem2.tag=='gain':
                            photo_config['gain']=elem2.text
                        if elem2.tag=='exposure':
                            photo_config['exposure']=elem2.text
                        if elem2.tag=='sharpness':
                            photo_config['sharpness']=elem2.text
                        if elem2.tag=='temperature':
                            photo_config['temperature']=elem2.text
                        if elem2.tag=='focus':
                            photo_config['focus']=elem2.text
                        if elem2.tag=='zoom':
                            photo_config['zoom']=elem2.text
                        if elem2.tag=='pan':
                            photo_config['pan']=elem2.text
                        if elem2.tag=='tilt':
                            photo_config['tilt']=elem2.text
                        if elem2.tag=='mirror':
                            photo_config['mirror']=elem2.text
                        if elem2.tag=='rotateup':
                            photo_config['rotateup']=elem2.text
                            # for elem3 in list(elem2):
                            #     if elem3.tag=='Room':
                            #         output['Room']=elem3.text
            print("\n")                     
            print(photo_config)
            print('Value of brightness:', photo_config.get('brightness'))
            print('Value of contrast:', photo_config.get('contrast'))
            print('Value of staturation:', photo_config.get('staturation'))
            print('Value of gain:', photo_config.get('gain'))
            print('Value of exposure:', photo_config.get('exposure'))
            print('Value of sharpness:', photo_config.get('sharpness'))
            print('Value of temperature:', photo_config.get('temperature'))
            print('Value of focus:', photo_config.get('focus'))
            print('Value of zoom:', photo_config.get('zoom'))
            print('Value of pan:', photo_config.get('pan'))
            print('Value of tilt:', photo_config.get('tilt'))
            print('Stage of mirror:', photo_config.get('mirror'))
            print('Stage of rotateup:', photo_config.get('rotateup'))
            
            # brightness_value = {key: photo_config[key] for key in photo_config.keys() & {'brightness'}}
            # print brightness and value                              
            # print(brightness_value)
            # print only value of brightness
            # print('Value of brightness:', brightness_value.get('brightness'))

            # contrast_value = {key: photo_config[key] for key in photo_config.keys() & {'contrast'}}                     
            # print(contrast_value)
            # print('Value of contrast:', contrast_value.get('contrast'))

            # staturation_value = {key: photo_config[key] for key in photo_config.keys() & {'staturation'}}                     
            # print(staturation_value)
            # print('Value of staturation:', staturation_value.get('staturation'))

            # gain_value = {key: photo_config[key] for key in photo_config.keys() & {'gain'}}                     
            # print(gain_value)
            # print('Value of gain:', gain_value.get('gain'))

            # exposure_value = {key: photo_config[key] for key in photo_config.keys() & {'exposure'}}                     
            # print(exposure_value)
            # print('Value of exposure:', exposure_value.get('exposure'))

            # sharpness_value = {key: photo_config[key] for key in photo_config.keys() & {'sharpness'}}                     
            # print(sharpness_value)
            # print('Value of sharpness:', sharpness_value.get('sharpness'))

            # temperature_value = {key: photo_config[key] for key in photo_config.keys() & {'temperature'}}                     
            # print(temperature_value)
            # print('Value of temperature:', temperature_value.get('temperature'))

            # focus_value = {key: photo_config[key] for key in photo_config.keys() & {'focus'}}                     
            # print(focus_value)
            # print('Value of focus:', focus_value.get('focus'))

            # zoom_value = {key: photo_config[key] for key in photo_config.keys() & {'zoom'}}                     
            # print(zoom_value)
            # print('Value of zoom:', zoom_value.get('zoom'))

            # pan_value = {key: photo_config[key] for key in photo_config.keys() & {'pan'}}                     
            # print(pan_value)
            # print('Value of pan:', pan_value.get('pan'))

            # tilt_value = {key: photo_config[key] for key in photo_config.keys() & {'tilt'}}                     
            # print(tilt_value)
            # print('Value of tilt:', tilt_value.get('tilt'))

            # mirror_value = {key: photo_config[key] for key in photo_config.keys() & {'mirror'}}                     
            # print(mirror_value)
            # print('Stage of mirror:', mirror_value.get('mirror'))

            # rotateup_value = {key: photo_config[key] for key in photo_config.keys() & {'rotateup'}}                     
            # print(rotateup_value)
            # print('Stage of rotateup:', rotateup_value.get('rotateup'))
    
    for elem in tree.getiterator():
        if elem.tag=='software':
            video_config={}
            for elem1 in list(elem):            
                if elem1.tag=='video':
                    for elem2 in list(elem1):
                        if elem2.tag=='mirror':
                            video_config['mirror']=elem2.text
                        if elem2.tag=='rotateup':
                            video_config['rotateup']=elem2.text
                        if elem2.tag=='blur':
                            video_config['blur']=elem2.text
                        if elem2.tag=='invert':
                            video_config['invert']=elem2.text
                        if elem2.tag=='mono':
                            video_config['mono']=elem2.text
            # if output[1]
            print("\n")
            print(video_config)
            print('Stage of mirror:', video_config.get('mirror'))
            print('Stage of rotateup:', video_config.get('rotateup'))
            print('Stage of blur:', video_config.get('blur'))
            print('Stage of invert:', video_config.get('invert'))
            print('Stage of mono:', video_config.get('mono'))

            # mirror_value = {key: video_config[key] for key in video_config.keys() & {'mirror'}}                     
            # print(mirror_value)
            # print('Stage of mirror:', mirror_value.get('mirror'))

            # rotateup_value = {key: video_config[key] for key in video_config.keys() & {'rotateup'}}                     
            # print(rotateup_value)
            # print('Stage of rotateup:', rotateup_value.get('rotateup'))

            # blur_value = {key: video_config[key] for key in video_config.keys() & {'blur'}}                     
            # print(blur_value)
            # print('Stage of blur:', blur_value.get('blur'))

            # invert_value = {key: video_config[key] for key in video_config.keys() & {'invert'}}                     
            # print(invert_value)
            # print('Stage of invert:', invert_value.get('invert'))

            # mono_value = {key: video_config[key] for key in video_config.keys() & {'mono'}}                     
            # print(mono_value)
            # print('Stage of mono:', mono_value.get('mono'))

# def getProfileDefault():
#     default_value = str('100', '100', '100', '25', '500', '50', '3500', '0', '0', '0', '0', 'Checked', 'Unchecked')
#     return default_value
def loadPhotoParameters(fileName):
    tree = parse(file_name)
    root = tree.getroot()

    for elem in tree.getiterator():
        if elem.tag=='software':
            photo_config={}
            for elem1 in list(elem):
                if elem1.tag=='photo':
                    for elem2 in list(elem1):
                        if elem2.tag=='brightness':
                            photo_config['brightness']=elem2.text
                        if elem2.tag=='contrast':
                            photo_config['contrast']=elem2.text
                        if elem2.tag=='staturation':
                            photo_config['staturation']=elem2.text
                        if elem2.tag=='gain':
                            photo_config['gain']=elem2.text
                        if elem2.tag=='exposure':
                            photo_config['exposure']=elem2.text
                        if elem2.tag=='sharpness':
                            photo_config['sharpness']=elem2.text
                        if elem2.tag=='temperature':
                            photo_config['temperature']=elem2.text
                        if elem2.tag=='focus':
                            photo_config['focus']=elem2.text
                        if elem2.tag=='zoom':
                            photo_config['zoom']=elem2.text
                        if elem2.tag=='pan':
                            photo_config['pan']=elem2.text
                        if elem2.tag=='tilt':
                            photo_config['tilt']=elem2.text
                        if elem2.tag=='mirror':
                            photo_config['mirror']=elem2.text
                        if elem2.tag=='rotateup':
                            photo_config['rotateup']=elem2.text
            print("\n")                     
            print(photo_config)
            brightness = photo_config.get('brightness')
            print('Value of brightness:', brightness)
            contrast = photo_config.get('contrast')
            print('Value of contrast:', contrast)
            staturation = photo_config.get('staturation')
            print('Value of staturation:', staturation)
            gain = photo_config.get('gain')
            print('Value of gain:', gain)
            exposure = photo_config.get('exposure')
            print('Value of exposure:', exposure)
            sharpness = photo_config.get('sharpness')
            print('Value of sharpness:', sharpness)
            focus =  photo_config.get('focus')
            print('Value of focus:', focus)
            zoom = photo_config.get('zoom')
            print('Value of zoom:', zoom)
            mirror = photo_config.get('mirror')
            print('Stage of mirror:', mirror)
            rotateup = photo_config.get('rotateup')
            print('Stage of rotateup:', rotateup)
            
            return brightness, contrast, staturation, gain, sharpness, focus, zoom, rotateup, rotateup

def loadVideoParameters(fileName):
    tree = parse(file_name)
    root = tree.getroot()    

    for elem in tree.getiterator():
        if elem.tag=='software':
            video_config={}
            for elem1 in list(elem):            
                if elem1.tag=='video':
                    for elem2 in list(elem1):
                        if elem2.tag=='mirror':
                            video_config['mirror']=elem2.text
                        if elem2.tag=='rotateup':
                            video_config['rotateup']=elem2.text
                        if elem2.tag=='blur':
                            video_config['blur']=elem2.text
                        if elem2.tag=='invert':
                            video_config['invert']=elem2.text
                        if elem2.tag=='mono':
                            video_config['mono']=elem2.text                            
            print("\n")
            print(video_config)
            mirror = video_config.get('mirror')
            print('Stage of mirror:', mirror)
            rotateup = video_config.get('rotateup')
            print('Stage of rotateup:', rotateup)
            blur = video_config.get('blur')
            print('Stage of blur:', blur)
            invert = video_config.get('invert')
            print('Stage of invert:', invert)
            mono = video_config.get('mono')
            print('Stage of mono:', mono)

            return rotateup, rotateup, blur, invert, mono

def getConfigName():
    config_name = ('brightness', 'contrast', 'staturation', 'gain', 'exposure',
                   'sharpness', 'temperature', 'focus', 'zoom', 'pan', 'tilt',
                   'mirror', 'rotateup', 'blur', 'invert', 'mono')
    return config_name

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def saveDefaultParameters(fileName):
    fileName = fileName
    # root = tree.getroot()

    # config_default = getProfileDefault()
    # config_name = getConfigName()
    data = Element('software')

    items0 = SubElement(data, 'name')
    items1 = SubElement(data, 'version')
    items2 = SubElement(data, 'copyright')
    items3 = SubElement(data, 'year')

    items4 = SubElement(data, 'photo')
    items5 = SubElement(data, 'video')

    # items_tab1 = SubElement(items4, 'config')
    # items_tab2 = SubElement(items5, 'config')

    # items parent contains
    sub_items_tab_1  = SubElement(items4,'brightness')
    sub_items_tab_2  = SubElement(items4,'contrast')
    sub_items_tab_3  = SubElement(items4,'staturation')
    sub_items_tab_4  = SubElement(items4,'gain')
    sub_items_tab_5  = SubElement(items4,'exposure')
    sub_items_tab_6  = SubElement(items4,'sharpness')
    sub_items_tab_7  = SubElement(items4,'focus')
    sub_items_tab_8  = SubElement(items4,'zoom')    
    sub_items_tab_9  = SubElement(items4,'mirror')
    sub_items_tab_10 = SubElement(items4,'rotateup')

    # sub_items_tab_7  = SubElement(items4,'temperature')
    # sub_items_tab_10 = SubElement(items4,'pan')
    # sub_items_tab_11 = SubElement(items4,'tilt')

    sub_items_tab1_1 = SubElement(items5,'mirror')
    sub_items_tab1_2 = SubElement(items5,'rotateup')
    sub_items_tab1_3 = SubElement(items5,'blur')
    sub_items_tab1_4 = SubElement(items5,'invert')
    sub_items_tab1_5 = SubElement(items5,'mono')
    
    # Name of sub items
    # sub_items_tab_1.set('name', 'brightness')
    # sub_items_tab_2.set('name', 'contrast')
    # sub_items_tab_3.set('name', 'staturation')
    # sub_items_tab_4.set('name', 'gain')
    # sub_items_tab_5.set('name', 'exposure')
    # sub_items_tab_6.set('name', 'sharpness')
    # sub_items_tab_7.set('name', 'temperature')
    # sub_items_tab_8.set('name', 'focus')
    # sub_items_tab_9.set('name', 'zoom')
    # sub_items_tab_10.set('name', 'pan')
    # sub_items_tab_11.set('name', 'tilt')
    # sub_items_tab_12.set('name', 'mirror')
    # sub_items_tab_13.set('name', 'rotateup')

    # sub_items_tab1_1.set('name', 'mirror')
    # sub_items_tab1_2.set('name', 'rotateup')
    # sub_items_tab1_3.set('name', 'blur')
    # sub_items_tab1_4.set('name', 'invert')
    # sub_items_tab1_5.set('name', 'mono')

    # Value
    items0.text = 'Camera Control'
    items1.text = '1.0.0'
    items2.text = 'Copyright 2021 - Co Bao Hieu'
    items3.text = '2020'

    default_value_brightness  = '128'
    default_value_contrast    = '128'
    default_value_staturation = '128'
    default_value_gain        = '25'
    default_value_exposure    = '-5'
    default_value_sharpness   = '128'
    default_value_focus       = '0'
    default_value_zoom        = '100'
    default_check_stage       = 'Checked'
    default_uncheck_stage     = 'Unchecked'

    sub_items_tab_1.text  = default_value_brightness
    sub_items_tab_2.text  = default_value_contrast
    sub_items_tab_3.text  = default_value_staturation
    sub_items_tab_4.text  = default_value_gain
    sub_items_tab_5.text  = default_value_exposure
    sub_items_tab_6.text  = default_value_sharpness
    sub_items_tab_7.text  = default_value_focus
    sub_items_tab_8.text  = default_value_zoom
    sub_items_tab_9.text  = default_check_stage
    sub_items_tab_10.text = default_uncheck_stage
    
    # sub_items_tab_7.text  = temperature
    # sub_items_tab_10.text = pan
    # sub_items_tab_11.text = tilt

    sub_items_tab1_1.text = default_check_stage
    sub_items_tab1_2.text = default_uncheck_stage
    sub_items_tab1_3.text = default_uncheck_stage
    sub_items_tab1_4.text = default_uncheck_stage
    sub_items_tab1_5.text = default_uncheck_stage

    # Create a new XML file with the results
    mydata = prettify(data)
    myfile = open(fileName, "w")
    myfile.write(mydata)
    myfile.close()

def saveFinalParameters(fileName, stream):
    # stream = cv2.VideoCapture(1)
    # print(stream)
    fileName = fileName
    # config_name = getConfigName()
    data = Element('software')

    items0 = SubElement(data, 'name')
    items1 = SubElement(data, 'version')
    items2 = SubElement(data, 'copyright')
    items3 = SubElement(data, 'year')

    items4 = SubElement(data, 'photo')
    items5 = SubElement(data, 'video')

    # items parent contains
    sub_items_tab_1  = SubElement(items4,'brightness')
    sub_items_tab_2  = SubElement(items4,'contrast')
    sub_items_tab_3  = SubElement(items4,'staturation')
    sub_items_tab_4  = SubElement(items4,'gain')
    sub_items_tab_5  = SubElement(items4,'exposure')
    sub_items_tab_6  = SubElement(items4,'sharpness')
    sub_items_tab_7  = SubElement(items4,'focus')
    sub_items_tab_8  = SubElement(items4,'zoom')    
    sub_items_tab_9  = SubElement(items4,'mirror')
    sub_items_tab_10 = SubElement(items4,'rotateup')

    sub_items_tab1_1 = SubElement(items5,'mirror')
    sub_items_tab1_2 = SubElement(items5,'rotateup')
    sub_items_tab1_3 = SubElement(items5,'blur')
    sub_items_tab1_4 = SubElement(items5,'invert')
    sub_items_tab1_5 = SubElement(items5,'mono')

    # Value
    items0.text = 'Camera Control'
    items1.text = '1.0.0'
    items2.text = 'Copyright 2021 - Co Bao Hieu'
    items3.text = '2020'

    brightness    = str(stream.get(cv2.CAP_PROP_BRIGHTNESS))
    contrast      = str(stream.get(cv2.CAP_PROP_CONTRAST))
    staturation   = str(stream.get(cv2.CAP_PROP_SATURATION))
    gain          = str(stream.get(cv2.CAP_PROP_GAIN))
    exposure      = str(stream.get(cv2.CAP_PROP_EXPOSURE))
    sharpness     = str(stream.get(cv2.CAP_PROP_SHARPNESS))
    focus         = str(stream.get(cv2.CAP_PROP_FOCUS))
    zoom          = str(stream.get(cv2.CAP_PROP_ZOOM))
    check_stage   = 'Checked'
    uncheck_stage = 'Unchecked'

    sub_items_tab_1.text  = brightness
    sub_items_tab_2.text  = contrast
    sub_items_tab_3.text  = staturation
    sub_items_tab_4.text  = gain
    sub_items_tab_5.text  = exposure
    sub_items_tab_6.text  = sharpness
    sub_items_tab_7.text  = focus
    sub_items_tab_8.text  = zoom
    sub_items_tab_9.text  = check_stage
    sub_items_tab_10.text = uncheck_stage

    sub_items_tab1_1.text = check_stage
    sub_items_tab1_2.text = uncheck_stage
    sub_items_tab1_3.text = uncheck_stage
    sub_items_tab1_4.text = uncheck_stage
    sub_items_tab1_5.text = uncheck_stage

    # Create a new XML file with the results
    mydata = prettify(data)
    myfile = open(fileName, "w")
    myfile.write(mydata)
    myfile.close()
    camera_control(stream)

def camera_control(stream):
    Window_name = "Demo"
    cv2.startWindowThread()
    while(True):
        # Capture frame-by-frame
        ret, frame = stream.read()
        
        # if the frame was not ret, then we have reached the end
        # of the stream
        if not ret:
            break

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # # Display the resulting frame
        # cv2.imshow(Window_name,gray)
        cv2.namedWindow(Window_name, cv2.WINDOW_NORMAL) 
        cv2.imshow(Window_name,frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # When everything done, release the capture
    stream.release()
    cv2.destroyWindow(Window_name)

if __name__ == "__main__":
    # saveDefaultParameters('config.xml')
    saveFinalParameters('config.xml', cv2.VideoCapture(1))
    # reading(file_name)