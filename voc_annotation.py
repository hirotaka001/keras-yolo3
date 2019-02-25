import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2007', 'train'), ('2007', 'trainval'), ('2007', 'val')]

classes = ["person"]


def convert_annotation(year, image_id, list_file):
    in_file = open('../aushop_fullbody_tx5vx01_20190110/Converted_Root/Annotations/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        occluded = obj.find('occluded').text
        cls = obj.find('name').text
        if cls not in classes or int(occluded)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('../aushop_fullbody_tx5vx01_20190110/Converted_Root/ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('../aushop_fullbody_tx5vx01_20190110/Converted_Root/JPEGImages/%s.jpg'%( image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

