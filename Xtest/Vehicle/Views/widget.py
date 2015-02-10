'''
Created on Feb 4, 2015

@author: rene
'''

from PySide import QtGui

from Xtest.Vehicle.Renderer.defaultRenderer import DefaultRenderer

class Widget(QtGui.QWidget):
    def __init__(self,name, tixi, tigl, data, parent = None):
        super(Widget, self).__init__(parent)
        
        # window preferences
        self.title = name
        self.width = 300
        self.height = 300
        self.resize(self.width ,self.height)
        
        self.setRenderer(self.width, self.height,tixi, tigl, data)
        
        # objects
        self.setWindowObjects()
        self.setContextMenu()
        
        self.setShowAircraft()
  
    def setRenderer(self, w, h, tixi, tigl, data):
        self.renderer = DefaultRenderer(self.getTitle(), w, h, tixi, tigl, data)
  
    def setWindowObjects(self):
        label1 = QtGui.QLabel("opacity")
        label5 = QtGui.QLabel("zoom")

        transparency = QtGui.QSpinBox()
        transparency.setRange(0, 100)
        transparency.setSingleStep(5)
        transparency.setSuffix('%')
        transparency.setValue(0)        
        transparency.valueChanged.connect(self.setTransparency)
      
        zoom = QtGui.QSpinBox()
        zoom.setRange(1, 100)
        zoom.setSingleStep(1)
        zoom.setSuffix('%')
        zoom.setValue(50)        
        zoom.valueChanged.connect(self.setZoom)      

        grid = QtGui.QGridLayout()
        grid.addWidget(transparency, 1,0)
        grid.addWidget(label1,       1,1)
        grid.addWidget(zoom,         1,2)
        grid.addWidget(label5,       1,3)

        grid.addWidget(self.renderer,4,0,1,10)

        self.setLayout(grid)
        
        # self.setFocusPolicy(QtCore.Qt.ClickFocus)
        #self.setSizePolicy (QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    def setContextMenu(self):
        # context menu
        self.menu = QtGui.QMenu(self)
        
        # context menu actions
        self.showOptions = [QtGui.QAction("Show fuselage", self), QtGui.QAction("Show wing1up", self),
                            QtGui.QAction("Show wing1lo", self), QtGui.QAction("Show wing2up", self),
                            QtGui.QAction("Show wing2lo", self), QtGui.QAction("Show components", self),
                            QtGui.QAction("Show TE_Device", self), QtGui.QAction("Show LE_Device", self),
                            QtGui.QAction("Show spoiler", self), QtGui.QAction("Show ribs", self),
                            QtGui.QAction("Show spars", self)]
        aircraftAction   =  QtGui.QAction("Show aircraft", self)

        # context menu add actions
        self.menu.addSeparator() 
        
        for i in range (len(self.showOptions)) :
            self.showOptions[i].setCheckable(True)
            self.menu.addAction(self.showOptions[i])

        self.menu.addSeparator()
        self.menu.addAction(aircraftAction)
        
        # connect actions with methods       
        self.showOptions[0].triggered.connect(self.setShowFuse) 
        self.showOptions[1].triggered.connect(self.setShowWing1up) 
        self.showOptions[2].triggered.connect(self.setShowWing1lo) 
        self.showOptions[3].triggered.connect(self.setShowWing2up) 
        self.showOptions[4].triggered.connect(self.setShowWing2lo) 
        self.showOptions[5].triggered.connect(self.setShowCompnt) 
        self.showOptions[6].triggered.connect(self.setShowFlapTE) 
        self.showOptions[7].triggered.connect(self.setShowFlapLE) 
        self.showOptions[8].triggered.connect(self.setShowFlapSpoiler) 
        self.showOptions[9].triggered.connect(self.setShowRibs) 
        self.showOptions[10].triggered.connect(self.setShowSpars)
        aircraftAction.triggered.connect(self.setShowAircraft)      
        
        # set check flags
        self.showOptions[0].setChecked(self.renderer.flag_show_fuselage) 
        self.showOptions[1].setChecked(self.renderer.flag_show_wing1_up) 
        self.showOptions[2].setChecked(self.renderer.flag_show_wing1_lo) 
        self.showOptions[3].setChecked(self.renderer.flag_show_wing2_up) 
        self.showOptions[4].setChecked(self.renderer.flag_show_wing2_lo) 
        self.showOptions[5].setChecked(self.renderer.flag_show_compnt) 
        self.showOptions[6].setChecked(self.renderer.flag_show_flap_TE_Device) 
        self.showOptions[7].setChecked(self.renderer.flag_show_flap_LE_Device) 
        self.showOptions[8].setChecked(self.renderer.flag_show_flap_spoiler) 
        self.showOptions[9].setChecked(self.renderer.flag_show_ribs) 
        self.showOptions[10].setChecked(self.renderer.flag_show_spars)
 
    def getTitle(self):
        return self.title
 
    def setTransparency(self, value):
        self.renderer.setTransparent(1.0 - value/100.0)
        self.renderer.updateGL()
        
    def setZoom(self, value):
        # slider range 1 to 100, therefor 50 is the center
        self.renderer.aspect = self.renderer.scale * ( (50.0-value) * 9.0/500.0 +1.0 )
        self.renderer.updateGL()
    
    def setShowFuse(self):
        self.renderer.flag_show_fuselage = not self.renderer.flag_show_fuselage

    def setShowWing1up(self):
        self.renderer.flag_show_wing1_up = not self.renderer.flag_show_wing1_up

    def setShowWing1lo(self):
        self.renderer.flag_show_wing1_lo = not self.renderer.flag_show_wing1_lo
        
    def setShowWing2up(self):
        self.renderer.flag_show_wing2_up = not self.renderer.flag_show_wing2_up
        
    def setShowWing2lo(self):
        self.renderer.flag_show_wing2_lo = not self.renderer.flag_show_wing2_lo
        
    def setShowCompnt(self):
        self.renderer.flag_show_compnt = not self.renderer.flag_show_compnt
    
    def setShowFlapLE(self):
        self.renderer.flag_show_flap_LE_Device = not self.renderer.flag_show_flap_LE_Device
    
    def setShowFlapTE(self):
        self.renderer.flag_show_flap_TE_Device = not self.renderer.flag_show_flap_TE_Device
    
    def setShowFlapSpoiler(self):
        self.renderer.flag_show_flap_spoiler = not self.renderer.flag_show_flap_spoiler
        
    def setShowSpars(self):
        self.renderer.flag_show_spars = not self.renderer.flag_show_spars
    
    def __setRotations(self, xRot, yRot, zRot):
        self.renderer.setXRotation(xRot)
        self.renderer.setYRotation(yRot)
        self.renderer.setZRotation(zRot)

    def __checkAircraft(self, vbool):
        self.renderer.flag_show_fuselage = vbool
        self.renderer.flag_show_wing1_up = vbool
        self.renderer.flag_show_wing1_lo = vbool
        self.renderer.flag_show_wing2_up = vbool
        self.renderer.flag_show_wing2_lo = vbool
        for i in range(5) : 
            self.showOptions[i].setChecked(vbool)
        
    def setShowAircraft(self):
        for i in range(5) : 
            if not self.showOptions[i].isChecked() :
                print ("setShowAircraft" , self.showOptions[i].isChecked())
                self.__checkAircraft(True) ; return
        self.__checkAircraft(False)
    
    def setShowRibs(self):
        self.renderer.flag_show_ribs = not self.renderer.flag_show_ribs


    def setTopView(self):
        self.renderer.setRotation(0, 0, 0)  
    
    def setFrontView(self):
        self.renderer.setRotation(90.0, 0, 270)  
    
    def setSideView(self):
        self.renderer.setRotation(90, 0, 0)       
    
    def set3DView(self):
        self.renderer.setRotation(45, 0, 315) 

    #===========================================================================
    # def setFlagSelection(self):
    #     self.renderer.flag_selection = not self.renderer.flag_selection
    #     self.renderer.selectedPoint = None
    #     self.renderer.updateLists()
    #===========================================================================
  
    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())

    def createSlider(self, setterSlot):
        slider = QtGui.QSpinBox()
        slider.setRange(0, 360)
        slider.setSingleStep(5)
        slider.valueChanged.connect(setterSlot)
        return slider