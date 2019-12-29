import xml.etree.ElementTree as ET
import os
import glob
import argparse

class_list_file = open('model_config/class.txt', 'r')
class_list = [line.split("\n")[0] for line in class_list_file.readlines()]

def get_file_name(file_name):
    in_file = open(file_name)
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    return os.path.basename(root.find('path').text)

def check_empty_voc(file_name):
    in_file = open(file_name)
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    if root.find('object') is None:
        return False
    
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        selected_cls = obj.find('name').text
        if selected_cls not in class_list or int(difficult) == 1:
            return False
    
    return True
        
def convert_annotation(file_name, write_file, image_file):
    in_file = open(file_name)
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        selected_cls = obj.find('name').text
        if selected_cls not in class_list or int(difficult) == 1:
            continue
        cls_id = class_list.index(selected_cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        gt = " " + ",".join([str(a) for a in b]) + ',' + str(cls_id)
        write_file.write(image_file)
        write_file.write(gt)
        write_file.write('\n')
        
if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument(
        '-a','--annotation', default=''
    )
    argparse.add_argument(
        '-w', '--write_path', default=''
    )

    args = argparse.parse_args()
    
    annotation_files = glob.glob(
        args.annotation + '*.xml'
    )
    
    new_annot_file = open(args.write_path, 'w')
    for annot_file in annotation_files:
        # base_name = os.path.basename(annot_file)
        # base_file = os.path.splitext(base_name)[0]
        base_file = get_file_name(annot_file)
        
        # image_file = 'data/aquarium/aquarium_mp4/' + base_file + '.jpg'
        image_file = 'data_scrapper/images/' + base_file 
        
        if check_empty_voc(annot_file):
            # new_annot_file = open(args.write_path + base_file + '.txt', 'w')
            convert_annotation(annot_file, new_annot_file, image_file)
            # new_annot_file.write('\n')
            
    new_annot_file.close()