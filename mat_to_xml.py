import os
from scipy import io
import numpy as np
from lxml import etree
from PIL import Image
from xml.etree.ElementTree import ElementTree

ROOT = os.getcwd()

pascal_part_path = 'Annotations_Part'
xml_file_path = '_xml_annotations'

mat_file_list = os.listdir(os.path.join(ROOT, pascal_part_path))
# global count_car, count_bus, count_file
count_car = count_bus = count_file = 0

def read_mat_file(filepath, _filename):
    global count_car, count_bus, count_file

    filename = _filename[:-4]
    mat_file = io.loadmat(os.path.join(filepath, filename))
    mat_data = mat_file['anno']
    is_car = False
    count_car = count_bus = 0
    xmin = []
    ymin = []
    xmax = []
    ymax = []


    # find class
    anno_object = np.ndarray.tolist(np.ndarray.tolist(mat_data)[0][0][1])[0]

    for i in range(len(anno_object)):
        objs_name = str(anno_object[i][0])[3:-2]

        if objs_name == 'car' or objs_name == 'bus':
            objs_part = np.ndarray.tolist(anno_object[i][3])
            if len(objs_part) == 0:
                continue

            for j in range(len(objs_part[0])):
                objs_part_name = str(objs_part[0][j][0])[3:-2]

                if objs_part_name == 'bliplate' or objs_part_name == 'fliplate':
                    if objs_name == 'car': count_car += 1
                    if objs_name == 'bus': count_bus += 1
                    is_car = True
                    plate_part_list = np.ndarray.tolist(objs_part[0][j][1])
                    width = len(plate_part_list[0])
                    height = len(plate_part_list)


                    is_break = False
                    for x in range(height):
                        for y in range(width):
                            if plate_part_list[x][y] == 1:
                                xmin.append(x)
                                ymin.append(y)
                                is_break = True
                                break
                        if is_break:
                            break

                    is_break = False
                    for _x in reversed(range(height)):
                        for _y in reversed(range(width)):
                            if plate_part_list[_x][_y] == 1:
                                xmax.append(_x)
                                ymax.append(_y)
                                is_break = True
                                break
                        if is_break:
                            break

    if is_car:
        count_file += 1
        return_list = [width, height, xmin, ymin, xmax, ymax]

        # make xml
        make_xml_file(return_list, filename)
        

def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def make_xml_file(_mat_list, _filename):

    width = _mat_list[0]   # type: int
    height = _mat_list[1]  # type: int
    xmin = _mat_list[2]    # type: list
    ymin = _mat_list[3]    # type: list
    xmax = _mat_list[4]    # type: list
    ymax = _mat_list[5]    # type: list

    root = etree.Element("annotation")

    folder = etree.SubElement(root, "folder")
    filename = etree.SubElement(root, "filename")

    folder.text = 'PascalPart'  # folder name is PscalPart
    filename.text = _filename + '.jpg'

    source = etree.SubElement(root, "source")

    # Set subElement of source
    s_database = etree.SubElement(source, "database")
    s_annotation = etree.SubElement(source, "annotation")
    s_image = etree.SubElement(source, "image")
    s_flickrid = etree.SubElement(source, "flickrid")

    s_database.text = 'The VOC2007 Database'
    s_annotation.text = 'PASCAL VOC2007'
    s_image.text = 'flickr'
    s_flickrid.text = _filename

    owner = etree.SubElement(root, "owner")

    # Set subElement of owner
    o_flickrid = etree.SubElement(owner, "flickrid")
    o_name = etree.SubElement(owner, "name")

    o_flickrid.text = 'ETRI'
    o_name.text = 'ETRI'

    size = etree.SubElement(root, "size")

    # Set subElement of size
    s_width = etree.SubElement(size, "width")
    s_height = etree.SubElement(size, "height")
    s_depth = etree.SubElement(size, "depth")

    w, h = width, height

    s_width.text, s_height.text = str(w), str(h)
    s_depth.text = '3'  # color image

    segmented = etree.Element("segmented")
    segmented.text = '0'

    object = etree.SubElement(root, "object")

    for i in range(len(xmin)):
        # Set subElement of object
        obj_name = etree.SubElement(object, "name")
        # obj_pose = etree.SubElement(object, "pose")
        # obj_truncated = etree.SubElement(object, "truncated")
        # obj_difficult = etree.SubElement(object, "difficult")
        obj_bndbox = etree.SubElement(object, "bndbox")

        obj_name.text = 'license plate'
        # obj_pose.text = ''
        # obj_truncated.text = ''
        # obj_difficult.text = ''

        # Set subElement of bndbox
        bnd_xmin = etree.SubElement(obj_bndbox, "xmin")
        bnd_ymin = etree.SubElement(obj_bndbox, "ymin")
        bnd_xmax = etree.SubElement(obj_bndbox, "xmax")
        bnd_ymax = etree.SubElement(obj_bndbox, "ymax")

        bnd_xmin.text = str(xmin[i])
        bnd_ymin.text = str(ymin[i])
        bnd_xmax.text = str(xmax[i])
        bnd_ymax.text = str(ymax[i])

    indent(root)

    ElementTree(root).write(os.path.join(xml_file_path, _filename + '.xml'))
    f = open(os.path.join(ROOT, '_file_info.txt'), 'a')
    text = '%s, %d, %d\n' %(_filename, count_car, count_bus)

    f.write(text)

    # f = open(os.path.join(ROOT, 'trainval', 'file_info'), 'w')
    # f.write(count_car + ' ' + count_bus + ' ' + count_file + '\n')
    # f.close()

def main():
    for name in mat_file_list:
        read_mat_file(os.path.join(ROOT, pascal_part_path), name)
    # read_mat_file(os.path.join(ROOT, pascal_part_path), '2009_004018.mat')
        



if __name__ == '__main__':
    main()