'''
Created on Aug 13, 2014

@author: fran_re
'''
class Config():
    path_cpacs_21_schema        = "configuration/cpacs_files/CPACS_21_Schema.xsd"
    path_cpacs_D150             = "configuration/cpacs_files/D150_CPACS2.0_valid.xml"
    path_cpacs_A320_Fuse        = "configuration/cpacs_files/A320_Fuse.xml"
    path_cpacs_A320_Wing        = "configuration/cpacs_files/A320_Wing.xml"
    
    path_code_completion_dict   = "configuration/keywords"
    
    path_element1               = "/plane/wings/wing[1]"
    path_element2               = "/cpacs/vehicles/aircraft/model/fuselages/fuselage[1]"
    
    attrName1                   = "position"
    attrName2                   = "uID"
    
    cpacs_default               =   "<?xml version=\"1.0\"?> \n" + \
                                    "    <cpacs> \n" + \
                                    "        <header> \n " + \
                                    "            <name></name> \n " + \
                                    "            <description></description> \n " + \
                                    "            <creator></creator> \n " + \
                                    "            <timestamp></timestamp> \n " + \
                                    "            <version></version> \n " + \
                                    "            <cpacsVersion></cpacsVersion> \n " + \
                                    "        </header> \n\n\n" + \
                                    "    </cpacs>"