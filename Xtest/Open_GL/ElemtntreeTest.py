'''
Created on Jul 25, 2014

@author: fran_re
'''
from lxml import etree

tree = etree.parse('/home/fran_re/workspace/Test/CPACS-Examples/sample.xml')

root = tree.getroot()

# root = etree.fromstring("sample_as_string")

print root.tag , root.attrib


for child in root:
    print child.tag, child.attrib

print root.tag   
print root[0][0].tag
print root[0][1].tag
print root[0][0].text
print root[1][0].text

'''
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''