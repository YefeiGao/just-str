#-*- coding:utf-8 -*-
import os
import os.path

ann_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image\\"
img_path = "home/gaoyefei/project/TextBoxes_plusplus-master/data/text/icpr2018/icpr2018_10k_image/"
xml_path = "home/gaoyefei/project/TextBoxes_plusplus-master/data/text/icpr2018/icpr2018_10k_anno_xml/"

def main():
    i = 1
    train_file = open('train.txt', 'w+')
    test_file = open('test.txt', 'w+')
    for files in os.walk(ann_path):
        for file in files[2]:
            print(file + "-->start!")
            img_name = os.path.splitext(file)[0]
            info = img_path + img_name + '.jpg' + ' ' + xml_path + img_name + '.xml' + '\n'
            if i % 4 == 0:
                test_file.write(info)
            else:
                train_file.write(info)
            i += 1

if __name__ == "__main__":
    main()