#-*- coding:utf-8 -*-

from xml.dom.minidom import Document
import os
import os.path
from PIL import Image

img_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image\\"
image_new_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image_renamed\\"
ann_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_txt\\"
xml_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_xml\\"

if not os.path.exists(xml_path):
    os.mkdir(xml_path)

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
        obj_list = line.split(',')
        print("element num is: {}".format(len(obj_list)))
        print(type(obj_list[-1]))
        print(obj_list[-1])
        # threes#
        object_new = doc.createElement("object")
        annotation.appendChild(object_new)

        name = doc.createElement('name')
        object_new.appendChild(name)
        name_txt = doc.createTextNode('text')
        name.appendChild(name_txt)

        content = doc.createElement('content')
        object_new.appendChild(content)
        content_txt = doc.createTextNode(obj_list[-1].strip())
        content.appendChild(content_txt)

        difficult = doc.createElement('difficult')
        object_new.appendChild(difficult)

        if obj_list[-1].encode('utf-8') == '###\n'.encode('utf-8'):
            difficult_txt = doc.createTextNode("1")
        else:
            difficult_txt = doc.createTextNode("0")
        difficult.appendChild(difficult_txt)

        # threes-1#
        bndbox = doc.createElement('bndbox')
        object_new.appendChild(bndbox)

        x1 = doc.createElement('x1')
        bndbox.appendChild(x1)
        x1_txt = doc.createTextNode(str(round(float(obj_list[2]))))
        x1.appendChild(x1_txt)

        y1 = doc.createElement('y1')
        bndbox.appendChild(y1)
        y1_txt = doc.createTextNode(str(round(float(obj_list[3]))))
        y1.appendChild(y1_txt)

        x2 = doc.createElement('x2')
        bndbox.appendChild(x2)
        x2_txt = doc.createTextNode(str(round(float(obj_list[4]))))
        x2.appendChild(x2_txt)

        y2 = doc.createElement('y2')
        bndbox.appendChild(y2)
        y2_txt = doc.createTextNode(str(round(float(obj_list[5]))))
        y2.appendChild(y2_txt)

        x3 = doc.createElement('x3')
        bndbox.appendChild(x3)
        x3_txt = doc.createTextNode(str(round(float(obj_list[6]))))
        x3.appendChild(x3_txt)

        y3 = doc.createElement('y3')
        bndbox.appendChild(y3)
        y3_txt = doc.createTextNode(str(round(float(obj_list[7]))))
        y3.appendChild(y3_txt)

        x4 = doc.createElement('x4')
        bndbox.appendChild(x4)
        x4_txt = doc.createTextNode(str(round(float(obj_list[0]))))
        x4.appendChild(x4_txt)

        y4 = doc.createElement('y4')
        bndbox.appendChild(y4)
        y4_txt = doc.createTextNode(str(round(float(obj_list[1]))))
        y4.appendChild(y4_txt)

        xmin = doc.createElement('xmin')
        bndbox.appendChild(xmin)
        xmin_txt = doc.createTextNode(str(round(min(min(float(obj_list[0]), float(obj_list[2])), min(float(obj_list[4]), float(obj_list[6]))))))
        xmin.appendChild(xmin_txt)

        ymin = doc.createElement('ymin')
        bndbox.appendChild(ymin)
        ymin_txt = doc.createTextNode(str(round(min(min(float(obj_list[1]), float(obj_list[3])), min(float(obj_list[5]), float(obj_list[7]))))))
        ymin.appendChild(ymin_txt)

        xmax = doc.createElement('xmax')
        bndbox.appendChild(xmax)
        xmax_txt = doc.createTextNode(str(round(max(max(float(obj_list[0]), float(obj_list[2])), max(float(obj_list[4]), float(obj_list[6]))))))
        xmax.appendChild(xmax_txt)

        ymax = doc.createElement('ymax')
        bndbox.appendChild(ymax)
        ymax_txt = doc.createTextNode(str(round(max(max(float(obj_list[1]), float(obj_list[3])), max(float(obj_list[5]), float(obj_list[7]))))))
        ymax.appendChild(ymax_txt)
        # threee-1#
        # threee#

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
            # lines = filelabel.read().split('\n')
            # obj = lines[:len(lines) - 1]

            # filename = xml_path + os.path.splitext(file)[0] + '.xml'
            filename = xml_path + str(i).zfill(6) + '.xml'
            # writeXml(temp, img_name, width, height, obj, filename)
            writeXml(temp, img_name, width, height, filename, filelabel)

        os.rmdir(temp)

if __name__ == "__main__":
    main()