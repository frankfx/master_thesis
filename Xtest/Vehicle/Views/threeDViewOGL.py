'''
Created on Jul 30, 2014

@author: fran_re
'''
from PySide import QtGui, QtCore
from Xtest.Vehicle.Views.widget import Widget
from Xtest.Vehicle.Renderer.threeDRenderer import ThreeDRenderer
    
class ThreeDViewOGL(Widget):
    def __init__(self,name, tixi, tigl, data, parent = None):
        super(ThreeDViewOGL, self).__init__(name, tixi, tigl, data, parent)
        self.set3DView()

    # override method 
    def setRenderer(self, w, h, tixi, tigl, data):
        self.renderer = ThreeDRenderer(w, h, tixi, tigl, data)

    # override method        
    def setWindowObjects(self):
        # window elements
        self.xSlider = self.createSlider(self.renderer.setXRotation)
        self.ySlider = self.createSlider(self.renderer.setYRotation)
        self.zSlider = self.createSlider(self.renderer.setZRotation)           
  
        label1 = QtGui.QLabel("opacity")
        label2 = QtGui.QLabel("xRot")
        label3 = QtGui.QLabel("yRot")
        label4 = QtGui.QLabel("zRot")
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

        grid.addWidget(self.xSlider ,1, 4)
        grid.addWidget(self.ySlider ,1, 6)
        grid.addWidget(self.zSlider ,1, 8)        
        grid.addWidget(label2       ,1, 5)
        grid.addWidget(label3       ,1, 7)
        grid.addWidget(label4       ,1, 9)        


        grid.addWidget(self.renderer,4,0,1,10)

        self.setLayout(grid)
        
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    # override method
    def setContextMenu(self):
        # context menu
        self.menu = QtGui.QMenu(self)        
        self.submenu_view = self.menu.addMenu("views")
        
        # context menu actions
        self.showOptions = [QtGui.QAction("Show fuselage", self), QtGui.QAction("Show wing1up", self),
                            QtGui.QAction("Show wing1lo", self), QtGui.QAction("Show wing2up", self),
                            QtGui.QAction("Show wing2lo", self), QtGui.QAction("Show components", self),
                            QtGui.QAction("Show TE_Device", self), QtGui.QAction("Show LE_Device", self),
                            QtGui.QAction("Show spoiler", self), QtGui.QAction("Show ribs", self),
                            QtGui.QAction("Show spars", self), QtGui.QAction("Show grid", self)]
        aircraftAction   =  QtGui.QAction("Show aircraft", self)        

        # context menu add actions
        self.menu.addSeparator() 
        
        self.viewOptions = [QtGui.QAction("top view", self), QtGui.QAction("front view", self),
                            QtGui.QAction("side view", self), QtGui.QAction("3D view", self)]
        
        for i in range(len(self.viewOptions)) :
            self.submenu_view.addAction(self.viewOptions[i])         

        for i in range (len(self.showOptions)) :
            self.showOptions[i].setCheckable(True)
            self.menu.addAction(self.showOptions[i])

        self.menu.addSeparator()
        self.menu.addAction(aircraftAction)
        
        self.viewOptions[0].triggered.connect(self.setTopView) 
        self.viewOptions[1].triggered.connect(self.setFrontView) 
        self.viewOptions[2].triggered.connect(self.setSideView) 
        self.viewOptions[3].triggered.connect(self.set3DView)   
        
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
        self.showOptions[11].triggered.connect(self.setShowGrid)     
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
        self.showOptions[10].setChecked(self.renderer.flag_show_grid)

    # override method    
    def setFrontView(self):
        self.xSlider.setValue(90) 
        self.zSlider.setValue(270)
    
    # override method    
    def setSideView(self):
        self.xSlider.setValue(90) 
    
    # override method    
    def set3DView(self):
        self.xSlider.setValue(45) 
        self.zSlider.setValue(315)        
       
    def setShowGrid(self):
        self.renderer.flag_show_grid = not self.renderer.flag_show_grid       
        