'''
Created on Aug 19, 2014

@author: fran_re
'''
from ctypes import *
from os import *

# define handles
cpacsHandle = c_int(0)
tixiHandle = c_int(0) # cint(0)
filename = "A320_Fuse.xml"
exportName = "./cpacsexample.iges"

# open TIXI and TIGL shared libraries
import sys
if sys.platform == 'win32':
    TIXI = cdll.TIXI
    TIGL = cdll.TIGL
else:
    TIXI = CDLL("libTIXI.so")
    TIGL = CDLL("libTIGL.so")


# Open a CPACS configuration file. First open the CPACS-XML file
# with TIXI to get a tixi handle and then use this handle to open
# and read the CPACS configuration.
tixiReturn = TIXI.tixiOpenDocument(filename, byref(tixiHandle))
if tixiReturn != 0:
    print 'Error: tixiOpenDocument failed for file: ' + filename
    exit(1)

tiglReturn = TIGL.tiglOpenCPACSConfiguration(tixiHandle, "Aircraft1_Fuselage1_Sec14", byref(cpacsHandle))

if tiglReturn != 0:
    TIXI.tixiCloseDocument(tixiHandle)
    print "Error: tiglOpenCPACSConfiguration failed for file: " + filename
    exit(1)
#------------------------------------
# Export CPACS geometry as IGES file.
#------------------------------------
print "Exporting CPACS geometry as IGES file..."
TIGL.tiglExportIGES(cpacsHandle, exportName)
