#### These utils are created to prepare the icpr2018 dataset for fine tuning the Textbox++ pre-trained model to improve the performance on Chinese character detection.

##### Three files are provided here as:
1. rename.py

- This script can be used to rename files in a folder with unrecognized characters.
2. txt2xml.py
- This script can be used to transform the annocation information with txt file to Pascal VOC style xml file. 
3. concatenate.py
- This script can be used to cancatenate image file path and corresponding xml file path for creating train.txt and test.txt files.
4. check_image_channel.py
- This script can be used to validate image struct for date cleaning process.