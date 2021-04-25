import sys
import os
import datetime
import time
import numpy
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

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom



sys.path.append(os.path.join(os.path.dirname(__file__), "./"))

# fileName = 'items.xml'
# tree = parse(fileName)

## Reading file
def reading(fileName):
    fileName = fileName
    root = tree.getroot()
    # One specific item attribute
    print('Item #2 attribute:')
    print(root[0][1].attrib)

    # All item attributes
    print('\nAll attributes:')
    for elem in root:
        for subelem in elem:
            print(subelem.attrib)

    # One sprecific item's data
    print('\nItem #2 data:')
    print(root[0][1].text)

    # All items data
    print('\nAll item data:')
    for elem in root:
        for subelem in elem:
            print(subelem.text)

## Counting Document
def counting(fileName):
    root = tree.getroot()
    print(len(root[0]))

## Writing document
def writing(fileName):
    fileName = fileName
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
    fileName = fileName
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
    fileName = fileName
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
    fileName = fileName
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

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def saveParameterFile(fileName):
    fileName = fileName
    # root = tree.getroot()
    data = Element('Parameters')
    items = SubElement(data, 'Configure')
    items1 = SubElement(data, 'SaveLoad')
    items2 = SubElement(data, 'Restore')


    items_tab = SubElement(items, 'Color')
    items_tab1 = SubElement(items1, 'Directory')
    items_tab2 = SubElement(items2, 'DefaultValues')

    # items parent contains
    sub_items_tab_1 = SubElement(items_tab,'Color')
    sub_items_tab_2 = SubElement(items_tab,'Color')
    sub_items_tab_3 = SubElement(items_tab,'Color')

    sub_items_tab1_1 = SubElement(items_tab,'Directory')

    sub_items_tab2_1 = SubElement(items_tab,'DefaultValues')
    sub_items_tab2_2 = SubElement(items_tab,'DefaultValues')
    sub_items_tab2_3 = SubElement(items_tab,'DefaultValues')

    # Name of sub items
    sub_items_tab_1.set('name', 'Red value')
    sub_items_tab_2.set('name', 'Green value')
    sub_items_tab_3.set('name', 'Blue value')

    sub_items_tab1_1.set('name', 'Path')

    sub_items_tab2_1.set('name', 'Red value')
    sub_items_tab2_2.set('name', 'Green value')
    sub_items_tab2_3.set('name', 'Blue value')

    # Value
    sub_items_tab_1.text = '255'
    sub_items_tab_2.text = '255'
    sub_items_tab_3.text = '255'

    sub_items_tab1_1.text = '/~/Documents/PixyMon/'

    sub_items_tab2_1.text = '0'
    sub_items_tab2_2.text = '0'
    sub_items_tab2_3.text = '0'

    # Create a new XML file with the results
    mydata = prettify(data)
    myfile = open(fileName, "w")
    myfile.write(mydata)
    myfile.close()
