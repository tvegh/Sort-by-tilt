import os
import Tkinter
import tkFileDialog
import subprocess
from lxml import etree

root = Tkinter.Tk()


def findFile():
    global fileDir
    global mainDir
    mainDir = os.getcwd()
    # save .p2vr file path
    fileDir = tkFileDialog.askopenfilename(
        parent=root, initialdir=mainDir, title='Please select the p2vr file')
    print('Found the .p2vr file')



# this takes in a hotspot XML element, then checks if there is a position/tilt element
# if there is one, return that value
# if there isnt one, it returns the next/tilt value
# this is here because polygon hotspots do not have position/tilt values
# which would cause the program not to work.
def hotspotTilt(hs):
    if (hs.find('./position/tilt') != None):
        return float(hs.find('./position/tilt').text)
    else:
        return float(hs.find('./next/tilt').text)


def sort():
    # Read the .p2vr file in
    with open(fileDir) as in_file:
        xml = etree.parse(in_file)
        xmlRoot = xml.getroot()
    # change the root to 'hotspots'
    xmlRoot = xmlRoot[0][5]

    # sort the data according tilt value
    xmlRoot[:] = sorted(xmlRoot[:], key=hotspotTilt)

    # Write the file out
    with open('sorted.p2vr', 'w') as out_file:
        xml.write(out_file)


findFile()
sort()
