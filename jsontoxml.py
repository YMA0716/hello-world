import json
import  os
import  xmltodict
from json import loads
from dicttoxml import  dicttoxml
from xml.dom.minidom import parseString

# json  转 xml
json_dir = '/home/myl/myl/workspace/newjiayin/'
xml_dir = '/home/myl/myl/workspace/testxml/'
jsonFiles = os.listdir(json_dir)
for file in jsonFiles:
    file_list = file.split(".")
    if (file_list[-1] == 'json'):
            json_path = json_dir + file
            xml_path = os.path.join(xml_dir, file_list[0] + '.xml')
            with open(json_path,'r',encoding= 'UTF-8') as json_file:
                # load_dict = loads(json_file.read())
                json_data = json.load(json_file)
                version = json_data["version"]
                flags = json_data["flags"]
                shapes = json_data["shapes"]
                xml = xmltodict.unparse({'Annotation':json_data},encoding= 'UTF-8')
                #print(version,flags,shapes)
                # my_item_func = lambda x: 'top' 'bottom'
                # xml = dicttoxml(json_data,custom_root='Annotation',item_func=my_item_func,attr_type = False)
                dom = parseString(xml)
                with open(xml_path,'w',encoding= 'UTF-8') as xml_file:
                     xml_file.write(dom.toprettyxml())

'''
[{'label': 'gangjuanneice',
  'points': [[1174.6610169491526, 440.22033898305085], [1635.677966101695, 1070.7288135593221]],
  'group_id': None, 'shape_type': 'rectangle', 'flags': {}}, 
{ 'label': 'biaoqian', 'points': [[1314.942528735632, 749.4252873563219], [1382.183908045977, 831.6091954022988]],
  'group_id': None,'shape_type': 'rectangle', 'flags': {}}]
'''
