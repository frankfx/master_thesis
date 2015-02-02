import os
'''
Created on Aug 13, 2014

@author: fran_re
'''
class Config():
    # path of the root directory
    path = os.path.dirname(__file__)
    
    #path to cpacs schema
    path_cpacs_21_schema = os.path.join(path, "external", "cpacs_files", "CPACS_21_Schema.xsd") 
    
    # D150 examples
    path_cpacs_D150   = os.path.join(path, "external", "cpacs_files","D150_CPACS2.0_valid.xml")
    path_cpacs_D150_2 = os.path.join(path, "external", "cpacs_files","D15d.xml")
    path_cpacs_D150_3 = os.path.join(path, "external", "cpacs_files","D150_CPACS2.0_valid3.xml") 

    # A320 Fuse and Wing example
    path_cpacs_A320_Fuse = os.path.join(path, "external","cpacs_files","A320_Fuse.xml")
    path_cpacs_A320_Wing = os.path.join(path, "external","cpacs_files","A320_Wing.xml") 
    
    # simple aircraft example
    path_cpacs_simple = os.path.join(path, "external","cpacs_files","simpletest.cpacs.xml")
    
    # output file
    path_cpacs_tmp_file = os.path.join(path, "external", "cpacs_files", "ToolOutput", "temp.xml")    
    path_cpacs_test     = os.path.join(path, "external", "cpacs_files", "ToolOutput", "test.xml")   
    path_cpacs_test2    = os.path.join(path, "external", "cpacs_files", "ToolOutput", "test2.xml")    
    path_cpacs_test3    = os.path.join(path, "external", "cpacs_files", "ToolOutput", "test3.xml") 
    
    # software
    path_saxon9he = os.path.join(path, "external", "software","saxon9he.jar") 
    
    # mappings
    path_cpacs_inputMapping  = os.path.join(path,"external", "mapping", "mappingInputRaw.xsl")    
    path_cpacs_outputMapping = os.path.join(path,"external", "mapping", "mappingOutputRaw.xsl")    

    # images
    path_but_right_icon = os.path.join(path,"external", "images", "buttonRightIcon.png")
    path_but_left_icon  = os.path.join(path,"external", "images", "buttonLeftIcon.png")
    
    # code completion directory
    path_code_completion_dict   = os.path.join(path, "XML_Editor", "configuration", "keywords")