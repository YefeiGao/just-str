#-*- coding:utf-8 -*-

from xml.dom.minidom import Document
import math
import os
import os.path
from PIL import Image
import numpy as np

global diff_cont, easy_cont
diff_cont = 0
easy_cont = 0

img_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image\\"
image_new_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image_renamed\\"
ann_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_txt\\"
xml_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_xml\\"

if not os.path.exists(xml_path):
    os.mkdir(xml_path)

'''Convert text annotation with anti-clockwise and confused starting point to constant clockwise
    and top-left, top-right, bottom-right, bottom-left turn.
    @postList: input quadrangle vertexes with continuous turn
    @orderedList: quadrangle vertexes with specific turn as top-left, top-right, bottom-right, bottom-left turn
'''
def orderedQuad(posList):
    # check if four vertexes are provided. where posList[0-7] corresponding to x1(0),y1(1),x2(2),y2(3),x3(4),y3(5),x4(6),y4(7)
    if len(posList) != 8:
        print('Bad data!')
        exit(0)
    # list for store ordered vertex
    orderedList = np.zeros((8, 1))

    # calculate endpoint of assistant axis
    # la: (x_la1, y_la1)->(x_la2, y_la2)
    x_la1 = (posList[0] + posList[2]) / 2
    y_la1 = (posList[1] + posList[3]) / 2
    x_la2 = (posList[4] + posList[6]) / 2
    y_la2 = (posList[5] + posList[7]) / 2

    # lb: (x_lb1, y_lb1)->(x_lb2, y_lb2)
    x_lb1 = (posList[2] + posList[4]) / 2
    y_lb1 = (posList[3] + posList[5]) / 2
    x_lb2 = (posList[0] + posList[6]) / 2
    y_lb2 = (posList[1] + posList[7]) / 2

    # component of direction vertor
    dire_la_x = (x_la2 - x_la1) / np.sqrt((x_la2 - x_la1) ** 2 + (y_la2 - y_la1) ** 2)
    dire_la_y = (y_la2 - y_la1) / np.sqrt((x_la2 - x_la1) ** 2 + (y_la2 - y_la1) ** 2)
    dire_la = [dire_la_x, dire_la_y]

    dire_lb_x = (x_lb2 - x_lb1) / np.sqrt((x_lb2 - x_lb1) ** 2 + (y_lb2 - y_lb1) ** 2)
    dire_lb_y = (y_lb2 - y_lb1) / np.sqrt((x_lb2 - x_lb1) ** 2 + (y_lb2 - y_lb1) ** 2)
    dire_lb = [dire_lb_x, dire_lb_y]

    # original point of new coordinate axis
    orig_x = (x_la1 + x_la2) / 2
    orig_y = (y_la1 + y_la2) / 2
    orignal = [orig_x, orig_y]

    # unit vector of old coordinate
    dire_x = [1, 0]
    dire_y = [0, 1]

    # angle between new and old coordinates
    angle_ax = np.dot(dire_x, dire_la)
    angle_ay = np.dot(dire_y, dire_la)
    angle_bx = np.dot(dire_x, dire_lb)
    angle_by = np.dot(dire_y, dire_lb)

    # assign axises with positive direction
    if abs(angle_ax) >= abs(angle_bx):
        if angle_ax < 0:
            dire_la = [-i for i in dire_la]
        if angle_by < 0:
            dire_lb = [-i for i in dire_lb]
        new_x = dire_la
        new_y = dire_lb
    else:
        if angle_ax < 0:
            dire_la = [-i for i in dire_la]
        if angle_by < 0:
            dire_lb = [-i for i in dire_lb]
        new_x = dire_lb
        new_y = dire_la

    # ascertain vertex with its position in new coordinate
    OP1 = list(map(lambda x: x[0] - x[1], zip([posList[0], posList[1]], orignal)))
    if np.dot(new_x, OP1) <= 0 and np.dot(new_y, OP1) <= 0:
        orderedList[0] = posList[0]
        orderedList[1] = posList[1]
    elif np.dot(new_x, OP1) >= 0 and np.dot(new_y, OP1) <= 0:
        orderedList[2] = posList[0]
        orderedList[3] = posList[1]
    elif np.dot(new_x, OP1) >= 0 and np.dot(new_y, OP1) >= 0:
        orderedList[4] = posList[0]
        orderedList[5] = posList[1]
    elif np.dot(new_x, OP1) <= 0 and np.dot(new_y, OP1) >= 0:
        orderedList[6] = posList[0]
        orderedList[7] = posList[1]
    else:
        print('error!!!')
        exit(-1)

    OP2 = list(map(lambda x: x[0] - x[1], zip([posList[2], posList[3]], orignal)))
    if np.dot(new_x, OP2) <= 0 and np.dot(new_y, OP2) <= 0:
        orderedList[0] = posList[2]
        orderedList[1] = posList[3]
    elif np.dot(new_x, OP2) >= 0 and np.dot(new_y, OP2) <= 0:
        orderedList[2] = posList[2]
        orderedList[3] = posList[3]
    elif np.dot(new_x, OP2) >= 0 and np.dot(new_y, OP2) >= 0:
        orderedList[4] = posList[2]
        orderedList[5] = posList[3]
    elif np.dot(new_x, OP2) <= 0 and np.dot(new_y, OP2) >= 0:
        orderedList[6] = posList[2]
        orderedList[7] = posList[3]
    else:
        print('error!!!')
        exit(-1)
    # OP3 = [posList[4], posList[5]] - orignal
    OP3 = list(map(lambda x: x[0] - x[1], zip([posList[4], posList[5]], orignal)))
    if np.dot(new_x, OP3) <= 0 and np.dot(new_y, OP3) <= 0:
        orderedList[0] = posList[4]
        orderedList[1] = posList[5]
    elif np.dot(new_x, OP3) >= 0 and np.dot(new_y, OP3) <= 0:
        orderedList[2] = posList[4]
        orderedList[3] = posList[5]
    elif np.dot(new_x, OP3) >= 0 and np.dot(new_y, OP3) >= 0:
        orderedList[4] = posList[4]
        orderedList[5] = posList[5]
    elif np.dot(new_x, OP3) <= 0 and np.dot(new_y, OP3) >= 0:
        orderedList[6] = posList[4]
        orderedList[7] = posList[5]
    else:
        print('error!!!')
        exit(-1)

    OP4 = list(map(lambda x: x[0] - x[1], zip([posList[6], posList[7]], orignal)))
    if np.dot(new_x, OP4) <= 0 and np.dot(new_y, OP4) <= 0:
        orderedList[0] = posList[6]
        orderedList[1] = posList[7]
    elif np.dot(new_x, OP4) >= 0 and np.dot(new_y, OP4) <= 0:
        orderedList[2] = posList[6]
        orderedList[3] = posList[7]
    elif np.dot(new_x, OP4) >= 0 and np.dot(new_y, OP4) >= 0:
        orderedList[4] = posList[6]
        orderedList[5] = posList[7]
    elif np.dot(new_x, OP4) <= 0 and np.dot(new_y, OP4) >= 0:
        orderedList[6] = posList[6]
        orderedList[7] = posList[7]
    else:
        print('error!!!')
        exit(-1)
    return orderedList

'''Convert txt file to xml file
'''
def writeXml(tmp, imgname, w, h, wxml, f):
    doc = Document()
    # owner
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    # owner
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_txt = doc.createTextNode("icpr2018_image_10k")
    folder.appendChild(folder_txt)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_txt = doc.createTextNode(imgname)
    filename.appendChild(filename_txt)

    # twos#
    size = doc.createElement('size')
    annotation.appendChild(size)

    width = doc.createElement('width')
    size.appendChild(width)
    width_txt = doc.createTextNode(str(w))
    width.appendChild(width_txt)

    height = doc.createElement('height')
    size.appendChild(height)
    height_txt = doc.createTextNode(str(h))
    height.appendChild(height_txt)

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_txt = doc.createTextNode("3")
    depth.appendChild(depth_txt)

    for line in f.readlines():
        obj_info = line.split(',')

        quad_info = [float(i) for i in obj_info[:8]]
        orderedList = orderedQuad(quad_info)
        orderedList = [math.floor(i) for i in orderedList]

        # check if exist out boundary
        orderedList[0] = max(orderedList[0], 0)
        orderedList[0] = min(orderedList[0], w)
        orderedList[1] = max(orderedList[1], 0)
        orderedList[1] = min(orderedList[1], h)

        orderedList[2] = max(orderedList[2], 0)
        orderedList[2] = min(orderedList[2], w)
        orderedList[3] = max(orderedList[3], 0)
        orderedList[3] = min(orderedList[3], h)

        orderedList[4] = max(orderedList[4], 0)
        orderedList[4] = min(orderedList[4], w)
        orderedList[5] = max(orderedList[5], 0)
        orderedList[5] = min(orderedList[5], h)

        orderedList[6] = max(orderedList[6], 0)
        orderedList[6] = min(orderedList[6], w)
        orderedList[7] = max(orderedList[7], 0)
        orderedList[7] = min(orderedList[7], h)

        x_loc_info = orderedList[0:7:2]
        y_loc_info = orderedList[1:8:2]

        content_info = obj_info[-1]

        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode('text')
        name.appendChild(name_txt)

        content = doc.createElement('content')
        object_new.appendChild(content)

        content_txt = doc.createTextNode(content_info.strip())
        content.appendChild(content_txt)

        difficult = doc.createElement('difficult')
        object_new.appendChild(difficult)

        if content_info.encode('utf-8') == '###\n'.encode('utf-8'):
            difficult_txt = doc.createTextNode("0")
            global diff_cont
            diff_cont += 1
        else:
            difficult_txt = doc.createTextNode("0")
            global easy_cont
            easy_cont += 1
        difficult.appendChild(difficult_txt)

        # threes-1#
        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)

        x1 = doc.createElement('x1')
        bndbox.appendChild(x1)
        # x1_txt = doc.createTextNode(str(round(float(obj_list[2]))))
        # x1_txt = doc.createTextNode(str(x_loc_info[0]))
        x1_txt = doc.createTextNode(str(orderedList[0]))
        x1.appendChild(x1_txt)

        y1 = doc.createElement('y1')
        bndbox.appendChild(y1)
        # y1_txt = doc.createTextNode(str(round(float(obj_list[3]))))
        # y1_txt = doc.createTextNode(str(y_loc_info[0]))
        y1_txt = doc.createTextNode(str(orderedList[1]))
        y1.appendChild(y1_txt)

        x2 = doc.createElement('x2')
        bndbox.appendChild(x2)
        # x2_txt = doc.createTextNode(str(round(float(obj_list[4]))))
        # x2_txt = doc.createTextNode(str(x_loc_info[3]))
        x2_txt = doc.createTextNode(str(orderedList[2]))
        x2.appendChild(x2_txt)

        y2 = doc.createElement('y2')
        bndbox.appendChild(y2)
        # y2_txt = doc.createTextNode(str(round(float(obj_list[5]))))
        # y2_txt = doc.createTextNode(str(y_loc_info[3]))
        y2_txt = doc.createTextNode(str(orderedList[3]))
        y2.appendChild(y2_txt)

        x3 = doc.createElement('x3')
        bndbox.appendChild(x3)
        # x3_txt = doc.createTextNode(str(round(float(obj_list[6]))))
        # x3_txt = doc.createTxtNode(str(x_loc_info[2]))
        x3_txt = doc.createTextNode(str(orderedList[4]))
        x3.appendChild(x3_txt)

        y3 = doc.createElement('y3')
        bndbox.appendChild(y3)
        # y3_txt = doc.createTextNode(str(round(float(obj_list[7]))))
        # y3_txt = doc.createTextNode(str(y_loc_info[2]))
        y3_txt = doc.createTextNode(str(orderedList[5]))
        y3.appendChild(y3_txt)

        x4 = doc.createElement('x4')
        bndbox.appendChild(x4)
        # x4_txt = doc.createTextNode(str(round(float(obj_list[0]))))
        # x4_txt = doc.createTextNode(str(x_loc_info[1]))
        x4_txt = doc.createTextNode(str(orderedList[6]))
        x4.appendChild(x4_txt)


        y4 = doc.createElement('y4')
        bndbox.appendChild(y4)
        # y4_txt = doc.createTextNode(str(round(float(obj_list[1]))))
        # y4_txt = doc.createTextNode(str(y_loc_info[1]))
        y4_txt = doc.createTextNode(str(orderedList[7]))
        y4.appendChild(y4_txt)

        xmin = doc.createElement('xmin')
        bndbox.appendChild(xmin)

        # xmin_txt = doc.createTextNode(str(round(min(min(float(obj_list[0]), float(obj_list[2])), min(float(obj_list[4]), float(obj_list[6]))))))
        xmin_txt = doc.createTextNode(str(min(x_loc_info)))
        xmin.appendChild(xmin_txt)

        ymin = doc.createElement('ymin')
        bndbox.appendChild(ymin)
        # ymin_txt = doc.createTextNode(str(round(min(min(float(obj_list[1]), float(obj_list[3])), min(float(obj_list[5]), float(obj_list[7]))))))
        ymin_txt = doc.createTextNode(str(min(y_loc_info)))
        ymin.appendChild(ymin_txt)

        xmax = doc.createElement('xmax')
        bndbox.appendChild(xmax)
        # xmax_txt = doc.createTextNode(str(round(max(max(float(obj_list[0]), float(obj_list[2])), max(float(obj_list[4]), float(obj_list[6]))))))
        xmax_txt = doc.createTextNode(str(max(x_loc_info)))
        xmax.appendChild(xmax_txt)

        ymax = doc.createElement('ymax')
        bndbox.appendChild(ymax)
        # ymax_txt = doc.createTextNode(str(round(max(max(float(obj_list[1]), float(obj_list[3])), max(float(obj_list[5]), float(obj_list[7]))))))
        ymax_txt = doc.createTextNode(str(max(y_loc_info)))
        ymax.appendChild(ymax_txt)

    tempfile = tmp + "test.xml"
    with open(tempfile, "wb+") as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
        # f.write(doc.toprettyxml(encoding='utf-8'))

    rewrite = open(tempfile, "r", encoding='utf-8')
    lines = rewrite.read().split('\n')
    newlines = lines[1:len(lines) - 1]

    fw = open(wxml, "w", encoding='utf-8')
    for i in range(0, len(newlines)):
        fw.write(newlines[i] + '\n')

    fw.close()
    rewrite.close()
    os.remove(tempfile)
    return

def main():
    i = 0
    j = 0
    for files in os.walk(ann_path):
        temp = "E:\\dataset\\icpr2018\\tmp\\"
        if not os.path.exists(temp):
            os.mkdir(temp)
        for file in files[2]:
            i += 1
            print(file + "-->start!")
            img_name = os.path.splitext(file)[0] + '.jpg'
            fileimgpath = img_path + img_name
            im = Image.open(fileimgpath)
            # im.save(new_fileimagepath)
            width = int(im.size[0])
            height = int(im.size[1])
            filelabel = open(ann_path + file, "r",encoding='utf-8')

            filename = xml_path + os.path.splitext(file)[0] + '.xml'
            # writeXml(temp, img_name, width, height, obj, filename)
            writeXml(temp, img_name, width, height, filename, filelabel)

        os.rmdir(temp)

if __name__ == "__main__":
    main()
    print("There have {} diffcult samples, and {} easy samples".format(diff_cont, easy_cont))
