'''
Created on Dec 3, 2014

@author: fran_re
'''

import sys
#from tiglwrapper   import Tigl, TiglException
#from tixiwrapper   import Tixi
from Xtest.Open_GL import utility
import time
import numpy as np
import math
from numpy import shape

class VehicleData():
    def __init__(self, tixi, tigl):
        
        __start_time = time.time()
        
        self.tixi = tixi
        self.tigl = tigl
        #self.__initTixiTigl()
        self.configurationGetLength = self.tigl.configurationGetLength() # 2.05436735655 ; D150 = 37.5708073949
        self.wingspan               = 0.0        
           
        utility.echo("Time after init tigl, tixi: " + str(time.time() - __start_time)) 
        self.pList_fuselage         = self.__createFuselage() 
        self.pList_fuselage_normals = self.createNormalList(self.pList_fuselage, True)
        utility.echo("Time after init fuselage: " + str(time.time() - __start_time) + ", compute: " + self.__cntPList(self.pList_fuselage) + " verts.")

        
        self.pList_wing_up, self.pList_wing_lo = self.__createWings()
        self.pList_wing_up_normals             = self.createNormalList(self.pList_wing_up, False)
        self.pList_wing_lo_normals             = self.createNormalList(self.pList_wing_lo, True)
        utility.echo("Time after wing one init : " + str(time.time() - __start_time) + ", compute: " + self.__cntPList(self.pList_wing_up) + " verts.")


        self.pList_wing_up_reflect, self.pList_wing_lo_reflect = self.__reflectWing(self.pList_wing_up, self.pList_wing_lo)
        self.pList_wing_up_reflect_normals                     = self.createNormalList(self.pList_wing_up_reflect, True)
        self.pList_wing_lo_reflect_normals                     = self.createNormalList(self.pList_wing_lo_reflect, False)
        utility.echo("Time after init wing two : " + str(time.time() - __start_time))

        self.pList_component_segment           = self.__createComponent()

        utility.echo("Time after component init : " + str(time.time() - __start_time))
        self.pList_flaps_TEDevice              = self.createFlaps(("trailingEdgeDevices", "trailingEdgeDevice"))
        self.pList_flaps_TE_normals            = self.createFlapNormals(self.pList_flaps_TEDevice)

        self.pList_flaps_LEDevice              =  self.createFlaps(("leadingEdgeDevices", "leadingEdgeDevice"))
        self.pList_flaps_LE_normals            = self.createFlapNormals(self.pList_flaps_LEDevice)

        self.pList_flaps_Spoiler               = self.createFlaps(("spoilers", "spoiler"))
        self.pList_flaps_Spoiler_normals       = self.createFlapNormals(self.pList_flaps_Spoiler)

#       self.plist_ribs                        = self.createRibs()
        self.pList_spares                      = self.createSpars()


        utility.echo("End data tigl calculation  -  Time: " + str(time.time() - __start_time))
    
    
    #------------------------------------------------- def __initTixiTigl(self):
        #---------------------------------------------------- self.tixi = Tixi()
        #----------------- self.tixi.open('../cpacs_files/simpletest.cpacs.xml')
        #------------- #self.tixi.open('../cpacs_files/D150_CPACS2.0_valid.xml')
#------------------------------------------------------------------------------ 
        #---------------------------------------------------- self.tigl = Tigl()
        #------------------------------------------------------------------ try:
            #-------------------------------------- self.tigl.open(self.tixi,"")
        #------------------------------------------ except TiglException as err:
            #-------------- print 'Error opening tigl document: ', err.__str__()

        
    # =========================================================================================================
    # =========================================================================================================    
    # code create point lists
    # =========================================================================================================  
    # =========================================================================================================
    
    '''
    create fuselage point List
    @param pnt_cnt_eta: stripe count
    @param pnt_cnt_zeta: point count per stripe
    '''
    def __createFuselage(self, pnt_cnt_eta = 1, pnt_cnt_zeta = 20):
        eta_List  = utility.createXcoordsLinear(1.0, pnt_cnt_eta)
        zeta_List = utility.createXcoordsLinear(1.0, pnt_cnt_zeta)        
        
        fuseList = []
        for fuseIdx in range(1, self.tigl.getFuselageCount()+1) :
            segList = []
            print self.tigl.fuselageGetSegmentCount(fuseIdx)+1
            for segIdx in range(1, self.tigl.fuselageGetSegmentCount(fuseIdx)+1) :
                stripeList = []
                for eta in eta_List :
                    stripe = []
                    for zeta in zeta_List :
                        x, y, z = self.tigl.fuselageGetPoint(fuseIdx, segIdx, eta, zeta)
                        stripe.append([x,y,z])
                    stripeList.append(stripe)
                segList.append(stripeList)
            fuseList.append(segList)
        return fuseList

    
    '''
    create wing point List
    @param pnt_cnt_eta: stripe count
    @param pnt_cnt_xsi: point count per stripe    
    '''    
    def __createWings(self, point_cnt_eta = 1, point_cnt_xsi = 10):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsCosineSpacing(1.0, point_cnt_xsi) 
                
        print self.tigl.wingGetSegmentCount(1)
                
        wingList_up = []            
        wingList_lo = []            
        for wingIdx in range(1, self.tigl.getWingCount()+1) :
            self.__setMaxWingSpan(wingIdx)
            segList_lo = [] 
            segList_up = []
            for segIdx in range(1, self.tigl.wingGetSegmentCount(wingIdx)+1) :
                stripeList_lo = [] 
                stripeList_up = []
                for eta in eta_List :
                    stripe_lo = []
                    stripe_up = []
                    for xsi in xsi_List :
                        x_l, y_l, z_l = self.tigl.wingGetLowerPoint(wingIdx, segIdx, eta, xsi)
                        x_u, y_u, z_u = self.tigl.wingGetUpperPoint(wingIdx, segIdx, eta, xsi)
                        stripe_lo.append([x_l, y_l, z_l])
                        stripe_up.append([x_u, y_u, z_u])
                    stripeList_lo.append(stripe_lo)    
                    stripeList_up.append(stripe_up)    
                segList_lo.append(stripeList_lo) 
                segList_up.append(stripeList_up)
            wingList_lo.append(segList_lo)
            wingList_up.append(segList_up)
        return wingList_up , wingList_lo

    '''
    reflect wing point list
    @param list1: upper wing point list
    @param list2: lower wing point list    
    ''' 
    def __reflectWing(self, list1, list2):
        wingList_up = []
        wingList_lo = []  
        for wingIdx in range(0, len(list1)):
            segList_up = []
            segList_lo = []
            for segIdx in range(0, len(list1[wingIdx])) :
                stripeList_lo = []
                stripeList_up = []                
                for stripeIdx in range(0, len(list1[wingIdx][segIdx])) :
                    stripe_lo = []
                    stripe_up = []                
                    for i in range(0, len(list1[wingIdx][segIdx][stripeIdx])):
                        tmp = list1[wingIdx][segIdx][stripeIdx][i]
                        stripe_up.append([tmp[0], -1*tmp[1], tmp[2]])
                        tmp = list2[wingIdx][segIdx][stripeIdx][i]
                        stripe_lo.append([tmp[0], -1*tmp[1], tmp[2]])
                    stripeList_lo.append(stripe_lo)
                    stripeList_up.append(stripe_up)
                segList_up.append(stripeList_up)
                segList_lo.append(stripeList_lo)
            wingList_up.append(segList_up)
            wingList_lo.append(segList_lo)
        return wingList_up, wingList_lo


    '''
    sets the wing span
    @param wingIdx: index of one wing   
    ''' 
    def __setMaxWingSpan(self, wingIdx):
        cur_wingspan = self.tigl.wingGetSpan(self.tigl.wingGetUID(wingIdx))
        max_wingspan = cur_wingspan if cur_wingspan > self.wingspan else self.wingspan
        self.wingspan =  max_wingspan

    '''
    create component segment point List
    @param pnt_cnt_eta: stripe count
    @param pnt_cnt_xsi: point count per stripe    
    '''
    def __createComponent(self, point_cnt_eta = 10, point_cnt_xsi = 11):
        eta_List = utility.createXcoordsLinear(1.0, point_cnt_eta)
        xsi_List = utility.createXcoordsLinear(1.0, point_cnt_xsi) 
             
        wingList = []   
        for wingIdx in range(1, self.tigl.getWingCount()+1) :
            segList = []
            for compSegIdx in range(1, self.tigl.wingGetComponentSegmentCount(wingIdx)+1) : 
                stripeList = []
                compSegUID = self.tigl.wingGetComponentSegmentUID(wingIdx, compSegIdx)
                for eta in eta_List :
                    stripe = []
                    for xsi in xsi_List :
                        x, y, z = self.tigl.wingComponentSegmentGetPoint(compSegUID, eta, xsi)
                        stripe.append([x, y, z])
                    stripeList.append(stripe)
                segList.append(stripeList)
            wingList.append(segList)
        return wingList
     
        
    '''
    create spar point List
    @param pnt_cnt_eta: stripe count
    @param pnt_cnt_xsi: point count per stripe    
    '''
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
                        
                      #  seg, wing = self.tigl.wingComponentSegmentFindSegment(componentSegmentUID, x1, y1, z1)
                      #  seg, wing =  self.tigl.wingGetSegmentIndex(seg)
                       # x1, y1, z1 = self.tigl.wingGetUpperPoint(wing, seg, spar[0], spar[1])     
                        
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
            sparPositionUIDs = []
            for sparPositionUIDIdx in range(1, self.tixi.getNumberOfChilds(path)+1) :
                sparPositionUIDs.append(self.tixi.getTextElement(path + 'sparPositionUID[' + str(sparPositionUIDIdx) + ']'))
            sparSegmentList.append(sparPositionUIDs)
        
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

    def __getSparPositionUIDs(self, wingIndex, compSegmentIndex):
        path_sparSegments = '/cpacs/vehicles/aircraft/model/wings/wing['\
                                +str(wingIndex)+']/componentSegments/componentSegment['\
                                +str(compSegmentIndex)+']/structure/spars/sparSegments/'
        
        path = path_sparSegments + 'sparSegment/@uID' 

        uidList = []
        for sparSegmentIdx in range(1, self.tixi.getNumberOfChilds(path_sparSegments)+1) :
            uidList.append(self.tixi.xPathExpressionGetTextByIndex(path, sparSegmentIdx))
        return uidList
    
    
    '''
    @param flapType: (parent, child)-String-Tuple of flap types, eg. ("trailingEdgeDevices","trailingEdgeDevice")
    '''
    def createFlaps(self, flapType):    
        (flapParent, _) = flapType

        plistWing = []        
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

                plistFlaps = []
                componentSegmentUID = self.tigl.wingGetComponentSegmentUID(wingIndex, compSegmentIndex)
                
                for flap in flapList : 

                    _, segUid1, eta1, xsi1 = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, flap[0], flap[2])       
                    _, segUid2, eta2, xsi2 = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, flap[1], flap[3]) 
                    _, segUid3, eta3, xsi3 = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, flap[4], flap[6]) 
                    _, segUid4, eta4, xsi4 = self.tigl.wingComponentSegmentPointGetSegmentEtaXsi(componentSegmentUID, flap[5], flap[7]) 
                    
                    (segIdx1, wingidx1) = self.tigl.wingGetSegmentIndex(segUid1)
                    (segIdx2, wingidx2) = self.tigl.wingGetSegmentIndex(segUid2)
                    (segIdx3, wingidx3) = self.tigl.wingGetSegmentIndex(segUid3)
                    (segIdx4, wingidx4) = self.tigl.wingGetSegmentIndex(segUid4)
                    
                    if eta1 < 0 : print "error" , eta1 ; eta1 = 0.0
                    
                    x1, y1, z1 = self.tigl.wingGetUpperPoint(wingidx1, segIdx1, eta1, xsi1)      
                    x2, y2, z2 = self.tigl.wingGetUpperPoint(wingidx2, segIdx2, eta2, xsi2)      
                    x3, y3, z3 = self.tigl.wingGetUpperPoint(wingidx3, segIdx3, eta3, xsi3)      
                    x4, y4, z4 = self.tigl.wingGetUpperPoint(wingidx4, segIdx4, eta4, xsi4)      
                          
                    # point on component segment
                    #x1, y1, z1 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[0], flap[2])       
                    #x2, y2, z2 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[1], flap[3]) 
                    #x3, y3, z3 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[4], flap[6]) 
                    #x4, y4, z4 = self.tigl.wingComponentSegmentGetPoint(componentSegmentUID, flap[5], flap[7]) 
                    # end 
                    
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


    '''
    creates a list of normals of a given point list
    @param plist: given point list
    @param flag: ???????????????
    '''  
    
    #TODO: complete ribs implementation
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

    def createFlapNormals(self, plist):
        shaList = [] ; segList = [] ; flapList = []
        for shape in plist :
            segList = []
            for seg in shape :
                flapList = []
                for flap in seg :
                    norm1 = self.__calculateVertexNormal(flap[0], flap[1], flap[2])
                    norm2 = self.__calculateVertexNormal(flap[1], flap[3], flap[0])
                    norm3 = self.__calculateVertexNormal(flap[3], flap[2], flap[1])
                    norm4 = self.__calculateVertexNormal(flap[2], flap[0], flap[3])
                    flapList.append([norm1, norm2, norm3, norm4])
                segList.append(flapList)
            shaList.append(segList)
        return shaList

    '''
    creates a list of normals of a given point list
    @param plist: given point list
    @param flag: ???????????????
    '''    
    def createNormalList(self, plist, flag):
        normalList = self.__createZeroPList(plist)
        
        shaIdx = -1
        for shape in plist :
            shaIdx += 1
            segCnt = len(shape)
            for segIdx in range(segCnt):
                stripeCnt = len(shape[segIdx])
                for stripeIdx in range(stripeCnt):
                    (tmp_seg , tmp_stripe) = (segIdx , stripeIdx+1) if stripeIdx +1 < stripeCnt else (segIdx+1 , 0)
                    if tmp_seg >= segCnt : break
                    
                    stripe1 = shape[segIdx][stripeIdx]
                    stripe2 = shape[tmp_seg][tmp_stripe]
                    pCnt = len(shape[segIdx][stripeIdx])

                    #flag2 = False                    
                    #if shape[segIdx][stripeIdx][0] == shape[segIdx][stripeIdx][pCnt-1] :
                    #    print "yea"
                    #flag2 = True
                    
                    for i in range(pCnt):
                        
                   #     if flag2:
                    #        if i == pCnt - 2 :
                     #           j = 0
                      #      else:                        
                        j = (i+1)%pCnt
                            
                         #   if i >= pCnt-1 :
                         #       normalList[shaIdx][segIdx][stripeIdx][i] = normalList[shaIdx][segIdx][stripeIdx][0]
                         #       normalList[shaIdx][tmp_seg][tmp_stripe][i] = normalList[shaIdx][tmp_seg][tmp_stripe][0]
                         #       break 
                        #else:
                         #   j = (i+1)%pCnt
                            
                        if flag:
                            norm1 = self.__calculateVertexNormal(stripe1[i], stripe2[i], stripe1[j])
                            norm2 = self.__calculateVertexNormal(stripe1[j], stripe1[i], stripe2[j])
                            norm3 = self.__calculateVertexNormal(stripe2[i], stripe2[j], stripe1[i])
                            norm4 = self.__calculateVertexNormal(stripe2[j], stripe1[j], stripe2[i])
                        else :
                            norm1 = self.__calculateVertexNormal(stripe1[i], stripe1[j], stripe2[i])
                            norm2 = self.__calculateVertexNormal(stripe1[j], stripe2[j], stripe1[i])
                            norm3 = self.__calculateVertexNormal(stripe2[i], stripe1[i], stripe2[j])
                            norm4 = self.__calculateVertexNormal(stripe2[j], stripe2[i], stripe1[j])
            
                        normalList[shaIdx][segIdx][stripeIdx][i]   = self.__add(normalList[shaIdx][segIdx][stripeIdx][i], norm1)
                        normalList[shaIdx][segIdx][stripeIdx][j]   = self.__add(normalList[shaIdx][segIdx][stripeIdx][j], norm2)
                        normalList[shaIdx][tmp_seg][tmp_stripe][i] = self.__add(normalList[shaIdx][tmp_seg][tmp_stripe][i], norm3)
                        normalList[shaIdx][tmp_seg][tmp_stripe][j] = self.__add(normalList[shaIdx][tmp_seg][tmp_stripe][j], norm4)
        return normalList


    '''
    copies a point list and sets all vertices to [0.0, 0.0, 0.0]
    @param plist: given point list
    '''        
    def __createZeroPList(self, plist):
        shaList = []
        for shape in plist :
            segList = []
            for seg in shape :
                stripeList = []
                for stripe in seg :
                    stripeList.append( [[0.0, 0.0, 0.0]]*len(stripe) )
                segList.append(stripeList)
            shaList.append(segList)
        return shaList        


    '''
    returns the point count of a given point list 
    @param plist: point list
    '''    
    def __cntPList(self, plist):
        res = 0
        for shape in plist :
            for seg in shape:
                for stripe in seg :
                    res += len(stripe)
        return str(res)
        
    def __printPlist(self, plist):
        for shape in plist :
            print "new shape"
            for seg in shape :
                print "new seg"
                for stripe in seg:
                    print stripe 
        
    '''
    get vertex normal in v1
    '''
    def __calculateVertexNormal(self, v1, v2, v3):
        edge1 = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
        edge2 = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]
        return self.__normalize(np.cross(edge1, edge2))
    
    def __add(self, vec1, vec2):
        return [vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]]    
    
    def __lenVector(self, v):
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        
    def __normalize(self, v):
        l = self.__lenVector(v)
        return [0.0, 0.0, 0.0] if l == 0.0 else [v[0] / l, v[1] / l, v[2] / l]  

# ======================================================================================================================================
# debug
# ====================================================================================================================================== 
#t = VehicleData()     
  
   