#-*- coding:utf-8 -*-
import os
import os.path
import cv2

img_path = "E:\\dataset\\icpr2018\\icpr2018_10k_image\\"

def main():
    i = 1
    # img = cv2.imread(img_path + '009129.jpg')
    # cv2.imshow('2016', img)
    # cv2.waitKey(0)
    for files in os.walk(img_path):
        for file in files[2]:
            # if i < 9600:
            #     i += 1
            #     continue
            print(file + "-->start!")
            img_name = os.path.splitext(file)[0] + '.jpg'
            fileimgpath = img_path + img_name

            try:
                img = cv2.imread(fileimgpath)
                # cv2.imshow('test', img)
                # cv2.waitKey(10)
            except:
                pass
            if img.shape[2] == 3:
                cv2.imshow('bad sample', img)
                cv2.waitKey(0)

if __name__ == "__main__":
    main()