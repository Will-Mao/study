# import xml.etree.ElementTree as etree
#
# etree.register_namespace('',"http://tempuri.org/")
# etree.register_namespace('a',"http://schemas.datacontract.org/2004/07/LandErp.ServiceModel")
# etree.register_namespace('a','a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight"')
# tree = etree.parse("matl.xml")
# root = tree.getroot()
# s = root.find("{http://tempuri.org/}se/{http://schemas.datacontract.org/2004/07/LandErp.ServiceModel}Asd")
# s = root.find('//se/Asd')
# b = s.find("{http://tempuri.org/}b")
# s[0].text = 'ss1'
# print(et.tostring(root, encoding='utf-8'))
# tree = et.ElementTree(root)
# tree.write('matl.xml', prety_print=False)
# print(s)

from lxml import etree
tree = etree.parse("matl.xml")
root = tree.getroot()
# se = root.find('se')
# ns = se.nsmap['a']
aa = root.xpath("//s:Asd",namespaces={'s':'http://schemas.datacontract.org/2004/07/LandErp.ServiceModel'})
# s = root.find('//se/Asd')
# s[0].text = 'ss1'
# tree.write('matl.xml', prety_print=False)
print(aa)

