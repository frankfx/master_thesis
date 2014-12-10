'''
Created on Dec 3, 2014

@author: fran_re
'''

import sys
from tiglwrapper   import Tigl, TiglException
from tixiwrapper   import Tixi
from Xtest.Open_GL import utility

class VehicleData():
    def __init__(self):
        
        self.tixi = Tixi()
        #self.tixi.open('simpletest.cpacs.xml')
        self.tixi.open('D150_CPACS2.0_valid.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
           
        self.pList_fuselage                    = self.createFuselage() 
        self.pList_wing_up, self.pList_wing_lo = self.createWing()
        
        print self.pList_wing_lo
        
        self.pList_wing_up_reflect, \
            self.pList_wing_lo_reflect         = self.__reflectWing(self.pList_wing_up, self.pList_wing_lo)
            
        self.pList_component_segment           = self.createComponent()
        self.pList_flaps_TEDevice              = self.createFlaps(("trailingEdgeDevices", "trailingEdgeDevice"))
        self.pList_flaps_LEDevice              = self.createFlaps(("leadingEdgeDevices", "leadingEdgeDevice"))
        self.pList_flaps_Spoiler               = self.createFlaps(("spoilers", "spoiler"))
        self.plist_ribs                        = self.createRibs()
        self.pList_spares                      = self.createSpars()
        
        self.configurationGetLength = self.tigl.configurationGetLength() # 2.05436735655 ; D150 = 37.5708073949
        
    # =========================================================================================================
    # =========================================================================================================    
    # code create point lists
    # =========================================================================================================  
    # =========================================================================================================
    
    '''
    create quad point list of fuselage for opengl 
    '''
    def createFuselage(self, point_cnt_eta = 1, point_cnt_zeta = 120):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        zeta_List = utility.createXcoordsLinear(1.0, point_cnt_zeta)        
        fuseList = []

        for fuseIdx in range(1, self.tigl.getFuselageCount()+1) :
            segList = []
            for segIdx in range(1, self.tigl.fuselageGetSegmentCount(fuseIdx)+1) :
                plist = []
                for etaIdx in range(0, len(eta_List)-1,1) :
                    for zetaIdx in range(0, len(zeta_List)-1,1) :
                        x1, y1, z1 = self.tigl.fuselageGetPoint(fuseIdx, segIdx, eta_List[etaIdx], zeta_List[zetaIdx])
                        x2, y2, z2 = self.tigl.fuselageGetPoint(fuseIdx, segIdx, eta_List[etaIdx], zeta_List[zetaIdx+1])
                        x3, y3, z3 = self.tigl.fuselageGetPoint(fuseIdx, segIdx, eta_List[etaIdx+1], zeta_List[zetaIdx+1])
                        x4, y4, z4 = self.tigl.fuselageGetPoint(fuseIdx, segIdx, eta_List[etaIdx+1], zeta_List[zetaIdx])
                        plist.append([x1,y1,z1]) ; plist.append([x2,y2,z2]) ; plist.append([x3,y3,z3]) ; plist.append([x4,y4,z4])
                segList.append(plist)
            fuseList.append(segList)
        return fuseList

    
    def createNormals(self, plist, point_cnt_eta, point_cnt_zeta):
        pass
        

    '''
    create quad point list of wing upper and lower side for opengl 
    '''    
    def createWing(self, point_cnt_eta = 1, point_cnt_xsi = 25):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsCosineSpacing(1.0, point_cnt_xsi) 
                
        wingList_up = []            
        wingList_lo = []            
        
        for wingIdx in range(1, self.tigl.getWingCount()+1) :
            segList_lo = [] ; segList_up = []
            for segIdx in range(1, self.tigl.wingGetSegmentCount(wingIdx)+1) :
                plist_lo = [] ; plist_up = []
                for etaIdx in range(0, len(eta_List)-1, 1) :
                    for xsiIdx in range(0, len(xsi_List)-1, 1) :
                        xu1, yu1, zu1 = self.tigl.wingGetUpperPoint(wingIdx, segIdx, eta_List[etaIdx], xsi_List[xsiIdx])
                        xu2, yu2, zu2 = self.tigl.wingGetUpperPoint(wingIdx, segIdx, eta_List[etaIdx], xsi_List[xsiIdx+1])
                        xu3, yu3, zu3 = self.tigl.wingGetUpperPoint(wingIdx, segIdx, eta_List[etaIdx+1], xsi_List[xsiIdx+1])
                        xu4, yu4, zu4 = self.tigl.wingGetUpperPoint(wingIdx, segIdx, eta_List[etaIdx+1], xsi_List[xsiIdx])
                        
                        xl1, yl1, zl1 = self.tigl.wingGetLowerPoint(wingIdx, segIdx, eta_List[etaIdx], xsi_List[xsiIdx])
                        xl2, yl2, zl2 = self.tigl.wingGetLowerPoint(wingIdx, segIdx, eta_List[etaIdx], xsi_List[xsiIdx+1])
                        xl3, yl3, zl3 = self.tigl.wingGetLowerPoint(wingIdx, segIdx, eta_List[etaIdx+1], xsi_List[xsiIdx+1])
                        xl4, yl4, zl4 = self.tigl.wingGetLowerPoint(wingIdx, segIdx, eta_List[etaIdx+1], xsi_List[xsiIdx])
                        
                        plist_up.append([xu1, yu1, zu1]) ; plist_up.append([xu2, yu2, zu2])
                        plist_up.append([xu3, yu3, zu3]) ; plist_up.append([xu4, yu4, zu4])
                        
                        plist_lo.append([xl1, yl1, zl1]) ; plist_lo.append([xl2, yl2, zl2])
                        plist_lo.append([xl3, yl3, zl3]) ; plist_lo.append([xl4, yl4, zl4])
                segList_lo.append(plist_lo) ; segList_up.append(plist_up)
            wingList_lo.append(segList_lo) ; wingList_up.append(segList_up)
        return wingList_up , wingList_lo

    '''
    create quad point list of component segment for opengl 
    '''
    def createComponent(self, point_cnt_eta = 1, point_cnt_xsi = 10):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsLinear(1.0, point_cnt_xsi) 
             
        wingList = []   
                    
        for wingIdx in range(1, self.tigl.getWingCount()+1) :
            segList = []
            for compSegIdx in range(1, self.tigl.wingGetComponentSegmentCount(wingIdx)+1) : 
                plist = []
                compSegUID = self.tigl.wingGetComponentSegmentUID(wingIdx, compSegIdx)
                for etaIdx in range(0, len(eta_List)-1,1) :
                    for xsiIdx in range(0, len(xsi_List)-1, 1) :
                        x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(compSegUID, eta_List[etaIdx], xsi_List[xsiIdx])
                        x2, y2, z2 = self.tigl.wingComponentSegmentGetPoint(compSegUID, eta_List[etaIdx], xsi_List[xsiIdx+1])
                        x3, y3, z3 = self.tigl.wingComponentSegmentGetPoint(compSegUID, eta_List[etaIdx+1], xsi_List[xsiIdx+1])
                        x4, y4, z4 = self.tigl.wingComponentSegmentGetPoint(compSegUID, eta_List[etaIdx+1], xsi_List[xsiIdx])
                        plist.append([x1,y1,z1]) ; plist.append([x2,y2,z2]) ; plist.append([x3,y3,z3]) ; plist.append([x4,y4,z4])
                segList.append(plist)
            wingList.append(segList)
        return wingList
        
    def __reflectWing(self, list1, list2):
        wingList_up = [] ; wingList_lo = []  
        for wingIdx in range(0, len(list1),1):
            segList_up = [] ; segList_lo = []
            for segIdx in range(0, len(list1[wingIdx]), 1) :
                plist_up = [] ; plist_lo = []
                for i in range(0, len(list1[wingIdx][segIdx]), 1):
                    tmp = list1[wingIdx][segIdx][i]
                    plist_up.append([tmp[0], -1*tmp[1], tmp[2]])
                    tmp = list2[wingIdx][segIdx][i]
                    plist_lo.append([tmp[0], -1*tmp[1], tmp[2]])
                segList_up.append(plist_up)
                segList_lo.append(plist_lo)
            wingList_up.append(segList_up)
            wingList_lo.append(segList_lo)
        return wingList_up, wingList_lo
        
    def createSpars(self):
        plistWing = []
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) :         
                try :
                    sparList = self.__createSpars(wingIndex, compSegmentIndex)
                except:
                    print "no spar for wing " + str(wingIndex) + " found." ; break
                
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                plistSparSeg = []
                for sparSegment in sparList : 
                    plistSpar = []
                    for spar in sparSegment :
                        x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, spar[0], spar[1])       
                        plistSpar.append([x1, y1, z1])
                    plistSparSeg.append(plistSpar)
                plistSeg.append(plistSparSeg)
            plistWing.append(plistSeg)      
            
        return plistWing   
                
    def __createSpars(self, wingIndex, compSegmentIndex):
        path_sparSegments = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/structure/spars/sparSegments/'

        sparSegmentList = []
        for sparSegmentIdx in range(1, self.tixi.getNumberOfChilds(path_sparSegments)+1) :
            path = path_sparSegments + 'sparSegment[' + str(sparSegmentIdx) + ']/sparPositionUIDs/' 
            sparPositionUIDsList = []
            for sparPositionUIDIdx in range(1, self.tixi.getNumberOfChilds(path)+1) :
                sparPositionUIDsList.append(self.tixi.getTextElement(path + 'sparPositionUID[' + str(sparPositionUIDIdx) + ']'))
            sparSegmentList.append(sparPositionUIDsList)
        
        sparList = []
        for sparSegment in sparSegmentList :
            plist = []
            for uid in sparSegment :
                path = self.tixi.uIDGetXPath(uid)
                eta = self.tixi.getDoubleElement(path + '/eta')
                xsi = self.tixi.getDoubleElement(path + '/xsi')
                plist.append([eta, xsi])
            sparList.append(plist)
            
        return sparList

    
    '''
    @param flapType: (parent, child)-String-Tuple of flap types, eg. ("trailingEdgeDevices","trailingEdgeDevice")
    '''
    def createFlaps(self, flapType, point_cnt_eta = 10, point_cnt_xsi = 10):    
        plistWing = []
        (flapParent, _) = flapType
        
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                try :
                    if flapParent == 'trailingEdgeDevices' : 
                        flapList = self.__createFlapsTE(wingIndex, compSegmentIndex)
                    elif flapParent == 'leadingEdgeDevices' :
                        flapList = self.__createFlapsLE(wingIndex, compSegmentIndex)
                    elif flapParent == 'spoilers' :
                        flapList = self.__createFlaps_Spoiler(wingIndex, compSegmentIndex)
                    else : print "unexpected behaviour in createFlaps" ; sys.exit()
                except:
                    print "no " + str(flapType) + " for wing " + str(wingIndex) + " found." ; break

                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                plistFlaps = []
                for flap in flapList : 
                    x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[0], flap[2])       
                    x2, y2, z2 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[1], flap[3]) 
                    x3, y3, z3 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[4], flap[6]) 
                    x4, y4, z4 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[5], flap[7]) 
                    plistFlaps.append([[x1, y1, z1], [x2, y2, z2], [x3, y3, z3], [x4, y4, z4]])
                plistSeg.append(plistFlaps)
            plistWing.append(plistSeg)      
        return plistWing             
    
    def __createFlapsTE(self, wingIndex, compSegmentIndex):
        path_TE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/trailingEdgeDevices/'
                                
        plistTE = []
        for _TE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_TE_Devices)+1) :
            path_in  = path_TE_Devices + 'trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/innerBorder/'
            path_out = path_TE_Devices + 'trailingEdgeDevice[' + str(_TE_Devices_Idx) + ']/outerShape/outerBorder/'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + 'etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + 'etaTE')
            xsiLE_in = self.tixi.getDoubleElement(path_in + 'xsiLE')
            xsiTE_in = 1.0               
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + 'etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + 'etaTE')
            xsiLE_out = self.tixi.getDoubleElement(path_out + 'xsiLE')
            xsiTE_out = 1.0
                    
            plistTE.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistTE     


    def __createFlapsLE(self, wingIndex, compSegmentIndex):
        path_LE_Devices = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/leadingEdgeDevices/'
                                
        plistLE = []
        for _LE_Devices_Idx in range(1, self.tixi.getNumberOfChilds(path_LE_Devices)+1) :
            path_in  = path_LE_Devices + 'leadingEdgeDevice[' + str(_LE_Devices_Idx) + ']/outerShape/innerBorder'
            path_out = path_LE_Devices + 'leadingEdgeDevice[' + str(_LE_Devices_Idx) + ']/outerShape/outerBorder'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
            xsiLE_in = 0.0 
            xsiTE_in = self.tixi.getDoubleElement(path_in + '/xsiTE')
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
            xsiLE_out = 0.0
            xsiTE_out = self.tixi.getDoubleElement(path_out + '/xsiTE')
                    
            plistLE.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistLE     


    def __createFlaps_Spoiler(self, wingIndex, compSegmentIndex):
        path_Spoiler = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/controlSurfaces/spoilers/'
        
        plistSpoiler = []
        for spoiler_Idx in range(1, self.tixi.getNumberOfChilds(path_Spoiler)+1) :
            path_in  = path_Spoiler + 'spoiler[' + str(spoiler_Idx) + ']/outerShape/innerBorder'
            path_out = path_Spoiler + 'spoiler[' + str(spoiler_Idx) + ']/outerShape/outerBorder'
                    
            etaLE_in = self.tixi.getDoubleElement(path_in + '/etaLE')
            etaTE_in = self.tixi.getDoubleElement(path_in + '/etaTE')
            xsiLE_in = self.tixi.getDoubleElement(path_in + '/xsiLE')
            xsiTE_in = self.tixi.getDoubleElement(path_in + '/xsiTE')
                    
            etaLE_out = self.tixi.getDoubleElement(path_out + '/etaLE')
            etaTE_out = self.tixi.getDoubleElement(path_out + '/etaTE')
            xsiLE_out = self.tixi.getDoubleElement(path_out + '/xsiLE')
            xsiTE_out = self.tixi.getDoubleElement(path_out + '/xsiTE')
                    
            plistSpoiler.append([etaLE_in, etaTE_in, xsiLE_in, xsiTE_in, etaLE_out, etaTE_out, xsiLE_out, xsiTE_out])
        return plistSpoiler  


    def createRibs(self):
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) :        
                try :
                    ribList = self.__createRibs(wingIndex, compSegmentIndex)
                except:
                    print "no ribs for wing " + str(wingIndex) + " found." ; break
                                
        return[]           
    
    def __createRibs(self, wingIndex, compSegmentIndex):
        path  = '/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/componentSegments/componentSegment['\
                                                                            +str(compSegmentIndex)+']/structure/'
        for idx_ribDef in range(1, self.tixi.getNumberOfChilds(path + 'ribsDefinitions/')+1) :    
            path_ribs_pos = path + 'ribsDefinitions/ribsDefinition[' + str(idx_ribDef) + ']/ribsPositioning/' 
            
            ribreference         = self.tixi.getTextElement(path_ribs_pos + "ribReference")
            etaStart             = self.tixi.getTextElement(path_ribs_pos + "etaStart")
            etaEnd               = self.tixi.getTextElement(path_ribs_pos + "etaEnd")
            ribStart             = self.tixi.getTextElement(path_ribs_pos + "ribStart")
            ribEnd               = self.tixi.getTextElement(path_ribs_pos + "ribEnd")
            numberOfRibs         = self.tixi.getTextElement(path_ribs_pos + "numberOfRibs")
            ribCrossingBehaviour = self.tixi.getTextElement(path_ribs_pos + "ribCrossingBehaviour")

                
            if ribStart == 'trailingEdge' :
                xsiStart = 0.0 ; xsiEnd = 0.0
            elif ribStart == 'leadingEdge' :
                xsiStart = 1.0 ; xsiEnd = 1.0
            elif ribStart in self.__getSparPositionUIDs(wingIndex, compSegmentIndex) :
                print "unimplemented now"
                pass

            if ribEnd == 'trailingEdge' :
                xsiStart = 0.0 ; xsiEnd = 0.0
            elif ribEnd == 'leadingEdge' :
                xsiStart = 1.0 ; xsiEnd = 1.0
            elif ribreference in self.__getSparPositionUIDs(wingIndex, compSegmentIndex) :
                path_spar_pos_uid = path + 'spars/sparSegments/sparSegment[' + ribreference +']/sparPositionUIDs/' 
                sparPositionUIDs = []
                for idx_spar_pos_uid in range(1, self.tixi.getNumberOfChilds(path_spar_pos_uid)+1) : 
                    sparPositionUIDs.append(self.tixi.getTextElement(path_spar_pos_uid + "sparPositionUID["+idx_spar_pos_uid+"]"))

                for idx_spar_pos in range(1, self.tixi.getNumberOfChilds(path + 'spars/sparPositions/')):
                    uid = self.tixi.xPathExpressionGetTextByIndex(path + 'spars/sparPositions/sparPosition/@uID', idx_spar_pos)
                    if uid in sparPositionUIDs :
                        eta = self.tixi.getTextElement(path + "spars/sparPositions/sparPosition[" + uid +"]/eta/")
                        xsi = self.tixi.getTextElement(path + "spars/sparPositions/sparPosition[" + uid +"]/xsi/")
                xsiStart = xsi ; xsiEnd = xsi              
                
            # (b - a) / (count of Points - 1)    
            spacing = (etaEnd - etaStart) / (numberOfRibs-1)
                
        return [] 

        
    def __getSparPositionUIDs(self, wingIndex, compSegmentIndex):
        path_sparSegments = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/structure/spars/sparSegments/'
        
        path = path_sparSegments + 'sparSegment/@uID' 

        uidList = []
        for sparSegmentIdx in range(1, self.tixi.getNumberOfChilds(path_sparSegments)+1) :
            uidList.append(self.tixi.xPathExpressionGetTextByIndex(path, sparSegmentIdx))
        return uidList

    