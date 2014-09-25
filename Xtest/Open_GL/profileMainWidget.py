'''
Created on Sep 2, 2014

@author: rene
'''
from Xtest.Open_GL import profileDetectorWidget
from Xtest.Open_GL.profile import Profile
import logging
import datetime
from Cython.Compiler.Nodes import OverrideCheckNode
'''
Created on Jul 30, 2014

@author: fran_re
'''
import sys
import math
from PySide import QtGui, QtCore

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                              "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info('\n#####################################################\nstart\n#####################################################')
logging.info(datetime.datetime.now().time())

class ProfileMainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ProfileMainWidget, self).__init__(parent)

        # ################################################
        logging.debug('call ProfileWidget__init__')
        # ################################################
        
        grid = QtGui.QGridLayout()
        
        self.ogl_widget          = ProfileWidget()
        self.ogl_widget_naca     = NacaWidget(self.ogl_widget) 
        self.ogl_widget_detector = ProfileDetectWidget(self.ogl_widget)
       
        self.ogl_widget_naca.butCreate.clicked.connect(self.updateEvalList)
        self.ogl_widget_detector.butCreate.clicked.connect(self.updateEvalList)
        
        grid.addLayout(self.createTopOfWidget(),0,1)
        grid.addWidget(self.ogl_widget, 1,1)

        self.setLayout(grid)
        self.updateEvalList()
        
        self.setWindowTitle('Profile-Widget')    
        self.resize(560,520)
        #self.setFixedSize(QtCore.QSize(400,400))
        self.show()
    
    
    def createTopOfWidget(self):
        vboxLayout  = QtGui.QVBoxLayout()
        vboxLayout.addWidget(self.createEvalView())
        vboxLayout.addWidget(self.createViewingElements())    
        return vboxLayout
        
    def createEvalView(self):
        groupEval    = QtGui.QGroupBox("Evaluation")
        gridEval    = QtGui.QGridLayout()
        
        labelName               = QtGui.QLabel("Name")
        labelLength             = QtGui.QLabel("Length")
        labelAngle              = QtGui.QLabel("Angle of attack")
        labelThickness          = QtGui.QLabel("Thickness")
        labelCamber             = QtGui.QLabel("Arch")
        self.textName           = QtGui.QLineEdit()
        self.textLength         = QtGui.QLineEdit()
        self.textAngle          = QtGui.QLineEdit()
        self.textThickness      = QtGui.QLineEdit()
        self.textCamber         = QtGui.QLineEdit()
        
        gridEval.addWidget(labelName                , 0, 0)
        gridEval.addWidget(labelLength              , 1, 0)
        gridEval.addWidget(labelAngle               , 2, 0)
        gridEval.addWidget(labelThickness           , 0, 3)
        gridEval.addWidget(labelCamber              , 1, 3)
        gridEval.addWidget(self.textName            , 0, 1)
        gridEval.addWidget(self.textLength          , 1, 1)
        gridEval.addWidget(self.textAngle           , 2, 1)
        gridEval.addWidget(self.textThickness       , 0, 4)
        gridEval.addWidget(self.textCamber          , 1, 4)
        
        self.textName.setReadOnly(True)
        self.textLength.setReadOnly(True)
        self.textAngle.setReadOnly(True)
        self.textThickness.setReadOnly(True)
        self.textCamber.setReadOnly(True)

        groupEval.setLayout(gridEval) 
        return groupEval    
        
    def createViewingElements(self):    
        groupView  = QtGui.QGroupBox("View") 
        gridView    = QtGui.QGridLayout()  
        
        checkShowPoints         = QtGui.QCheckBox("Show points")
        checkFitToPage          = QtGui.QCheckBox("Fit to page")
        checkCloseTrailingedge  = QtGui.QCheckBox("Close Trailing edge")
        checkChaikinCurve       = QtGui.QCheckBox("Chaikin curve ")
        checkDrawCamber         = QtGui.QCheckBox("Camber")
        checkDrawChord          = QtGui.QCheckBox("Chord")
        
        
        self.butNaca            = QtGui.QPushButton("NacaCreator")
        self.butImgDetect       = QtGui.QPushButton("ImgDetect")
        self.spinBoxRot         = QtGui.QDoubleSpinBox() 
        self.slider_zoom        = QtGui.QSlider(QtCore.Qt.Horizontal, self)     
        
        gridView.addWidget(self.slider_zoom         , 0, 1,1,2)
        gridView.addWidget(checkShowPoints          , 1, 0)
        gridView.addWidget(checkCloseTrailingedge   , 1, 1)        
        gridView.addWidget(checkFitToPage           , 2, 0)
        gridView.addWidget(checkChaikinCurve        , 2, 1)
        gridView.addWidget(checkDrawCamber          , 3, 0)
        gridView.addWidget(checkDrawChord           , 3, 1)
        gridView.addWidget(self.spinBoxRot          , 1, 2, 2, 1) 
        
        gridView.addWidget(self.butNaca             , 1, 4)
        gridView.addWidget(self.butImgDetect        , 2, 4)  

        self.spinBoxRot.setStyleSheet("QDoubleSpinBox { border: 3px inset grey; } \
            QDoubleSpinBox::up-button { subcontrol-position: left; width: 30px; height: 25px;} \
            QDoubleSpinBox::down-button { subcontrol-position: right; width: 30px; height: 25px;}")     
         
        self.spinBoxRot.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxRot.setRange(0,45)
        self.spinBoxRot.valueChanged.connect(self.fireSetRotValue)

        self.slider_zoom.setMinimum(1)
        self.slider_zoom.setValue(51)
        self.slider_zoom.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_zoom.valueChanged[int].connect(self.ogl_widget.setScale)         

        checkShowPoints.toggled.connect(self.fireShowPoints)
        checkFitToPage.toggled.connect(self.fireFitToPage)
        checkCloseTrailingedge.toggled.connect(self.fireCloseTrailingEdge)
        checkChaikinCurve.toggled.connect(self.fireChaikinCurve)
        checkDrawCamber.toggled.connect(self.fireDrawCamber)
        checkDrawChord.toggled.connect(self.fireDrawChord)

        self.butNaca.clicked.connect(self.fireNacaWidget)
        self.butImgDetect.clicked.connect(self.fireDetectWidget)    
    
        groupView.setLayout(gridView)     
        return groupView
    
    def updateEvalList(self):      
        self.textName.setText(self.ogl_widget.getName())
        self.textLength.setText(str(self.ogl_widget.getLenChord()))
        self.textAngle.setText(str(self.ogl_widget.getWorkAngle()))
        self.textThickness.setText(str(self.ogl_widget.getProfileThickness()))
        self.textCamber.setText(str(self.ogl_widget.getProfileArch()))

    def fireSetRotValue(self, value):
        self.ogl_widget.setRotate(-value)
        self.updateEvalList()
   
    def fireShowPoints(self, value):
        self.ogl_widget.setDrawPointsOption(value)   

    def fireFitToPage(self, value):
        if value:
            self.slider_zoom.setValue(51) 
            self.slider_zoom.setEnabled(False)
        else:
            self.slider_zoom.setEnabled(True)
        self.ogl_widget.fitToPage(value)  
    
    def fireCloseTrailingEdge(self, value):
        self.ogl_widget.setFlagCloseTrailingEdge(value)
    
    def fireChaikinCurve(self, value):
        self.ogl_widget.setFlagChaikinCurve(value)
    
    def fireDrawCamber(self, value):
        self.ogl_widget.setFlagDrawCamber(value)
        
    def fireDrawChord(self, value):    
        self.ogl_widget.setFlagDrawChord(value)
    
    def fireNacaWidget(self):
        self.ogl_widget_naca.show()

    def fireDetectWidget(self):
        self.ogl_widget_detector.show()

    def closeEvent(self, event):
        self.ogl_widget_naca.close()
        self.ogl_widget_detector.close()
        event.accept() # let the window close


class ProfileWidget(Profile):
    def __init__(self):
        Profile.__init__(self)
        
        self.resize(320,320)
        self.setMinimumHeight(200)
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

    def drawProfile(self):
        trX, trY = self.norm_vec_list(self.dataSet.getCompletePointList())
       

        GL.glTranslatef(1,0,0)
        GL.glRotate(self.getRotAngle(), 0,0,1)
        GL.glTranslatef(-1,0,0)
       # GL.glTranslatef(-trX, trY, 0) 
        
        GL.glColor3f(0, 0, 1)
        
        plist = self.dataSet.getSplineCurve() if self.getFlagSplineCurve() else self.dataSet.getCompletePointList()  
        
        GL.glBegin(GL.GL_LINE_STRIP) 
        for p in plist :
            GL.glVertex3f(p[0], p[1], p[2])              
        GL.glEnd()            

        if self.getFlagDrawCamber() :      
            self.drawCamber() 

        if self.getFlagDrawChord() :
            self.drawChord()

        #The Trailing edge
        if self.getFlagCloseTrailingEdge() :
            self.drawTrailingEdge(self.dataSet.getTrailingEdge())

        #The following code displays the control points as dots.
        if self.getFlagDrawPoints() :
            self.drawPoints(plist)
            
    def drawTrailingEdge(self, p):
        plist = self.dataSet.getPointList()
        p1 = plist[0]
        p2 = plist[len(plist)-1]
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glVertex3f(p1[0], p1[1], p1[2])
        GL.glVertex3f(p[0], p[1], p[2])
        GL.glVertex3f(p2[0], p2[1], p2[2])
        GL.glEnd()        

    def drawPoints(self, plist):
        GL.glPointSize(5.0)        
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_POINTS)
        for p in plist : 
            GL.glVertex3f(p[0], p[1], p[2])
        GL.glEnd()        
            

    # ================================================================================================================
    # profile generator
    # ================================================================================================================
    '''
    @summary: generating naca airfoils, based on http://en.wikipedia.org/wiki/NACA_airfoil    
    '''
    def createSym_Naca(self, length, thickness, pcnt=10):
        res_top = []
        res_bot = []
    
        c = length
        t = thickness
        plist = self.__createXcoords(c, pcnt)
    
        for x in plist:
            y = self.__computeY_t(x, c, t) 
            res_top.append([x,  y, 0])
            res_bot.append([x, -y, 0])
        
        res_bot.reverse()    
        self.setPointList(res_bot + res_top[1:])
        self.dataSet.updatePointListCamber()
        self.dataSet.updatePointListsForNaca()
        self.updateGL()

    def createCambered_Naca(self, length, thickness, maxCamber, posMaxCamber, pcnt=10):
        res_top = []
        res_bot = []     
        res_camber = []   
        
        plist = self.__createXcoords(length, pcnt)
        for x in plist :
            y_t = self.__computeY_t(x, length, thickness)
            y_c = self.__computeY_c(x, length, maxCamber, posMaxCamber)
            theta = self.__computeCamber(x, length, maxCamber, posMaxCamber)
            
            x_u = x - y_t * math.sin(theta)
            x_l = x + y_t * math.sin(theta)
            y_u = y_c + y_t * math.cos(theta)
            y_l = y_c - y_t * math.cos(theta)
            
            res_top.append([x_u, y_u, 0])
            res_bot.append([x_l, y_l, 0])
            res_camber.append([x, y_c, 0])
        res_bot.reverse()

        self.setPointList(res_bot + res_top[1:])      
        self.setPointListCamber(res_camber)
        self.dataSet.updatePointListsForNaca()
        self.updateGL()
           
    def __computeCamber(self, x, length, maxCamber, posMaxCamber):
        p = posMaxCamber
        m = maxCamber
        c = length
        
        if x >= 0 and x <= p*c :
            res = (2*m)/(p*p) * (p - x/c)
        elif x >= p*c and x <= c :
            res = 2*m / ((1-p)*(1-p)) * (p - x/c)
        else :
            return None
        return math.atan(res)
    
    def __computeY_c(self, x, length, maxCamber, posMaxCamber):
        m = maxCamber
        p = posMaxCamber
        c = length
        
        if x >= 0 and x < p*c :
            y = m * (x / (p*p)) * (2 * p - x / c) 
        elif x >= p*c and x <= c :
            
            print "((1-p)*(1-p)) * (1 + x/c - 2*p)"
            print "p (==posMaxCamber) = " , p , "x = " , x , "c (==length) = " , c ,
            
            y = m * ((c-x) / ((1-p)*(1-p))) * (1 + x/c - 2*p)
        return y
    
    def __computeY_t(self, x, c, t):
        tmp = -0.1036 if (x/c) == 1 else -0.1015
        y = t/0.2 * c * math.fabs( ( 0.2969  * math.sqrt(x/c)   +
                        (-0.1260) * (x/c)            +
                        (-0.3516) * math.pow(x/c, 2) +
                        ( 0.2843) * math.pow(x/c, 3) +
                        (tmp)     * math.pow(x/c, 4)) )        
        return y

    def __createXcoords(self, dist=1.0, point_cnt=35):
        interval = dist/ point_cnt
        
        res = [0]
        for i in range(0, point_cnt):
            p = round(res[i] + interval, 3)
            if p < dist : 
                res.append(p)
            elif p == dist : 
                res.append(p)
                return res
            else :
                break
        res.append(dist)
        return res         


class NacaWidget(QtGui.QWidget):
    def __init__(self, ogl_widget, parent = None):
        super(NacaWidget, self).__init__(parent)
        grid = QtGui.QGridLayout()
        self.setSizePolicy ( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        
        label1 = QtGui.QLabel("Name")
        label2 = QtGui.QLabel("Length")
        label3 = QtGui.QLabel("Max. Camber")
        label4 = QtGui.QLabel("Pos. max. Camber")
        label5 = QtGui.QLabel("Thickness")
        label6 = QtGui.QLabel("Number of points")
        
        label3_1 = QtGui.QLabel("First digit. %d to %s%%:" % (0, "9.5"))
        label4_1 = QtGui.QLabel("Second digit. %d to %d%%:" % (1, 9))
        label5_1 = QtGui.QLabel("Third & fourth digit. %d to %d%%:" % (1, 40))
        label6_1 = QtGui.QLabel("%d to %d" % (20, 200))
        
        self.text1Name = QtGui.QLineEdit()
        self.text1Name.setText('NACA 00xx')
        self.text1Name.setReadOnly(True)
        self.text2Length = QtGui.QLineEdit()
        self.text2Length.setText('1.0') 
        self.text2Length.setReadOnly(True)               
        self.text3MaxCamber = QtGui.QLineEdit()
        self.text3MaxCamber.setText('0')
        self.text4PosCamber = QtGui.QLineEdit()
        self.text4PosCamber.setText('0')
        self.text5Thickness = QtGui.QLineEdit()
        self.text5Thickness.setText('12') 
        
        self.countSpinBox = QtGui.QSpinBox()
        self.countSpinBox.setRange(20, 200)
        self.countSpinBox.setSingleStep(5)
        self.countSpinBox.setSuffix('pts')
        self.countSpinBox.setSpecialValueText("Automatic")
        self.countSpinBox.setValue(10)
        
        self.butCreate = QtGui.QPushButton("create")
        self.butCreate.clicked.connect(self.fireButtonCreate)
        self.ogl_widget = ogl_widget
        
        grid.addWidget(label1, 1, 1)
        grid.addWidget(label2, 2, 1)
        grid.addWidget(label3, 3, 1)
        grid.addWidget(label4, 4, 1)
        grid.addWidget(label5, 5, 1)
        grid.addWidget(label6, 6, 1)
        grid.addWidget(self.text1Name,      1, 3)
        grid.addWidget(self.text2Length,    2, 3)        
        grid.addWidget(self.text3MaxCamber, 3, 3)
        grid.addWidget(self.text4PosCamber, 4, 3)        
        grid.addWidget(self.text5Thickness, 5, 3)
        grid.addWidget(self.countSpinBox,   6, 3)
        grid.addWidget(label3_1, 3, 4)
        grid.addWidget(label4_1, 4, 4)
        grid.addWidget(label5_1, 5, 4)
        grid.addWidget(label6_1, 6, 4)
        
        grid.addWidget(self.butCreate, 7, 1)
        self.setLayout(grid)        

    def fireButtonCreate(self):
        
        length      = self.text2Length.text()
        maxCamber   = self.text3MaxCamber.text()
        posCamber   = self.text4PosCamber.text()        
        thick       = self.text5Thickness.text()
        pcnt        = self.countSpinBox.value()
        
        try : 
            length      = float(length)
            maxCamber   = float(maxCamber)
            posCamber   = float(posCamber)
            thick       = float(thick)
            
            if maxCamber == 0 :
                posCamber = 0 
                self.text4PosCamber.setText('0')
               
            if maxCamber > 9.5 or maxCamber < 0 :
                self.text3MaxCamber.selectAll() 
                return
            elif posCamber > 9 :
                self.text4PosCamber.selectAll()
                return
            elif maxCamber != 0 and posCamber < 1 :
                self.text4PosCamber.selectAll()
                return            
            elif thick > 40 or thick < 1 : 
                self.text5Thickness.selectAll()
                return
             
            if thick < 10 :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + '0' + str(int(thick)))    
            else :
                self.text1Name.setText('NACA ' + str(int(maxCamber)) + str(int(posCamber)) + str(int(thick)))
        except ValueError:
            print "fireButtonCreate in profileWidget (NACA Creator)" , length, thick
            return
        
        if maxCamber > 0 or posCamber > 0 :
            self.ogl_widget.createCambered_Naca(length, thick/100.0, maxCamber/100.0, posCamber/10.0, pcnt)
        else :
            self.ogl_widget.createSym_Naca(length, thick/100.0, pcnt)
        
        self.ogl_widget.setName(self.text1Name.text())


class ProfileDetectWidget(QtGui.QWidget): 
    def __init__(self, ogl_widget, parent = None):
        super(ProfileDetectWidget, self).__init__(parent)
        
        grid                     = QtGui.QGridLayout()
        label1                   = QtGui.QLabel("Name")
        self.text1Name           = QtGui.QLineEdit()       
        self.butCreate           = QtGui.QPushButton("create")
        self.butDetect           = QtGui.QPushButton("detect")
        self.butCancel           = QtGui.QPushButton("cancel")        
        self.ogl_widget          = ogl_widget
        self.ogl_detector_widget = profileDetectorWidget.ProfileDetectorWidget()
        #self.ogl_widget.setFixedSize(200,200)
        
        grid.addWidget(self.ogl_detector_widget, 1,1,1,5)
        grid.addWidget(label1,                       2,1)
        grid.addWidget(self.text1Name,               2,2)
        grid.addWidget(self.butCreate,               2,3)
        grid.addWidget(self.butDetect,               2,4)
        grid.addWidget(self.butCancel,               2,5)
        
        self.butCreate.clicked.connect(self.fireButtonCreate)
        self.butDetect.clicked.connect(self.fireButtonDetect)
        self.butCancel.clicked.connect(self.fireButtonClose)
        
        self.createActions()
        self.createMenus()
        
        self.setLayout(grid) 
        self.resize(420,320)
        
    def fireButtonCreate(self):
        name = self.text1Name.text() if self.text1Name.text() == "" else "untitled"
        self.ogl_widget.setName(name)
        self.ogl_widget.setPointList(self.ogl_detector_widget.getPointList())
       # self.ogl_widget.set_pointList_top(self.ogl_detector_widget.getPointList_top)
       # self.ogl_widget.set_pointList_bot(self.ogl_detector_widget.getPointList_bot)
        print "dummy function"

    def fireButtonDetect(self):
        if False: 
            ()
        else:
            self.ogl_detector_widget.flagDrawDefaultProfile = True
            self.ogl_detector_widget.updateGL()

    def fireButtonClose(self):
        self.ogl_detector_widget.flagDrawDefaultProfile = False
        self.close()

    def open(self) :
        (fileName, _) = QtGui.QFileDialog.getOpenFileName(self,
                                     "Open File", QtCore.QDir.currentPath())
        
        if (fileName) :
            print fileName
            #---------------------------------------------- if (image is None) :
                #----------- QtGui.QMessageBox.information(self, "Image Viewer",
                                         #------ "Cannot load " + str(fileName))
                #-------------------------------------------------------- return
    
            #self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
           # self.scaleFactor = 1.0
    
            #self.printAct.setEnabled(True)
           # self.fitToWindowAct.setEnabled(True)
            #self.updateActions()

           # if (not self.fitToWindowAct.isChecked()) :
            #   self.imageLabel.adjustSize()
            self.ogl_detector_widget.drawImage(fileName)

    def createActions(self):
        self.openAct = QtGui.QAction('Open...', self)
        self.openAct.triggered.connect(self.open)    
        
        self.exitAct = QtGui.QAction("E&xit", self);
        self.exitAct.triggered.connect(self.close)
        
    def createMenus(self):
        fileMenu = QtGui.QMenu("File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        menubar = QtGui.QMenuBar(self)
        menubar.addMenu(fileMenu)



if __name__ == '__main__':
    app = QtGui.QApplication(["PyQt OpenGL"])
    widget = ProfileMainWidget()
    widget.show()
    app.exec_()    