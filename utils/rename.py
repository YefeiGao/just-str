# -*- coding:utf-8 -*-
'''This script
'''
import sys
import os

i = 0
anno_txt_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_txt\\"
anno_txt_new_path = "E:\\dataset\\icpr2018\\icpr2018_10k_anno_txt_renamed\\"

for files in os.walk(anno_txt_path):
    for file in files[2]:
        i += 1
        if os.path.isfile(os.path.join(anno_txt_path, file)) == True:
            new_name = str(i).zfill(6) + '.txt'
            os.rename(os.path.join(anno_txt_path, file), os.path.join(anno_txt_new_path, new_name))