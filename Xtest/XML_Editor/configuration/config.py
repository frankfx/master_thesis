'''
Created on Aug 13, 2014

@author: fran_re
'''
class Config():
    path_cpacs_21_schema        = "../cpacs_files/CPACS_21_Schema.xsd"
    path_cpacs_D150             = "../cpacs_files/D150_CPACS2.0_valid.xml"
    path_cpacs_A320_Fuse        = "../cpacs_files/A320_Fuse.xml"
    path_cpacs_A320_Wing        = "../cpacs_files/A320_Wing.xml"
    path_cpacs_tmp_file         = "../cpacs_files/temp.xml"
    path_cpacs_simple           = "../cpacs_files/simpletest.cpacs.xml"
    
    path_cpacs_test           = "../../../cpacs_files/test.xml"   
    path_cpacs_inputMapping   = "../../../cpacs_files/mappingInputRaw.xsl"   
    path_cpacs_outputMapping  = "../../../cpacs_files/mappingOutputRaw.xsl"   
    path_cpacs_D150_2         = "../../../cpacs_files/D150_CPACS2.0_valid2.xml"   
    path_cpacs_D150_3         = "../../../cpacs_files/D150_CPACS2.0_valid3.xml"   
    
    path_but_right_icon       = "../../../images/buttonRightIcon.png"
    path_but_left_icon        = "../../../images/buttonLeftIcon.png"
    
    
    path_code_completion_dict   = "configuration/keywords"
    
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