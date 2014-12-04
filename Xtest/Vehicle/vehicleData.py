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
       # self.tixi.open('simpletest.cpacs.xml')
        self.tixi.open('D150_CPACS2.0_valid.xml')
        
        self.tigl = Tigl()
        try:
            self.tigl.open(self.tixi,"")
        except TiglException as err:    
            print 'Error opening tigl document: ', err.__str__()
           
        self.pList_fuselage                    = self.createFuselage() 
        self.pList_wing_up                     = []
        self.pList_wing_lo                     = []
        self.pList_wing_up, self.pList_wing_lo = self.createWing()
        self.pList_component_segment           = self.createComponent()
        self.pList_flaps_TEDevice              = self.createFlaps(("trailingEdgeDevices", "trailingEdgeDevice"))
        self.pList_flaps_LEDevice              = self.createFlaps(("leadingEdgeDevices", "leadingEdgeDevice"))
        self.pList_flaps_Spoiler               = self.createFlaps(("spoilers", "spoiler"))
        self.plist_ribs                        = self.createRibs()
        self.pList_spares                      = self.createSpars()
        
    # =========================================================================================================
    # =========================================================================================================    
    # code create point lists
    # =========================================================================================================  
    # =========================================================================================================
    def createFuselage(self, point_cnt_eta = 1, point_cnt_zeta = 45):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        zeta_List = utility.createXcoordsLinear(1.0, point_cnt_zeta) 
        
        plistFuse = []
        
        for fuselageIndex in range(1, self.tigl.getFuselageCount()+1) :
            plistSeg = []
            for segmentIndex in range(1, self.tigl.fuselageGetSegmentCount(fuselageIndex)+1) :
                #plistprofile = []
                for eta in eta_List :
                    plist = []
                    for zeta in zeta_List :
                        x, y, z = self.tigl.fuselageGetPoint(fuselageIndex, segmentIndex, eta, zeta)
                        plist.append([x,y,z])
                    #plistprofile.append(plist)
                    plistSeg.append(plist)
                #plistSeg.append(plistprofile)    
            plistFuse.append(plistSeg)        
        
        return plistFuse 


    def createWing(self, point_cnt_eta = 3, point_cnt_xsi = 20):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsCosineSpacing(1.0, point_cnt_xsi) 
                    
        plistWing_up = []
        plistWing_lo = []
        
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg_up = []
            plistSeg_lo = []
            for segmentIndex in range(1, self.tigl.wingGetSegmentCount(wingIndex)+1) :
                for eta in eta_List :
                    p_tmp_up = []
                    p_tmp_lo = []
                    for xsi in xsi_List :   
                        xu, yu, zu = self.tigl.wingGetUpperPoint(wingIndex, segmentIndex, eta, xsi)
                        xl, yl, zl = self.tigl.wingGetLowerPoint(wingIndex, segmentIndex, eta, xsi)
                        p_tmp_up.append([xu,yu,zu])
                        p_tmp_lo.append([xl,yl,zl])
                    plistSeg_up.append(p_tmp_up)
                    plistSeg_lo.append(p_tmp_lo)
            plistWing_up.append(plistSeg_up)
            plistWing_lo.append(plistSeg_lo)
            
        return plistWing_up , plistWing_lo


    def createComponent(self, point_cnt_eta = 10, point_cnt_xsi = 10):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsLinear(1.0, point_cnt_xsi) 
             
        plistComp = []     
                    
        for wingIndex in range(1, self.tigl.getWingCount()+1) :
            plistSeg = []
            for compSegmentIndex in range(1, self.tigl.wingGetComponentSegmentCount(wingIndex)+1) : 
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                for eta in eta_List :
                    p_tmp = []
                    for xsi in xsi_List :
                        x, y, z = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, eta, xsi)
                        p_tmp.append([x,y,z])
                    plistSeg.append(p_tmp)
            plistComp.append(plistSeg)
        return plistComp
        
        
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

    