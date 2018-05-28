# This script only includes detection.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# %matplotlib inline
import time
import math
import json
from nms import nms
from crop_image import crop_image

# Make sure that caffe is on the python path:
caffe_root = './'  # this file is expected to be in {caffe_root}/examples
import os
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

import cv2
from PIL import Image, ImageFont, ImageDraw
font = ImageFont.truetype('simhei.ttf', size=16)

# CRNN module
sys.path.append(caffe_root)
from crnn.crnnport import *
model,converter = crnnSource()

# global transformer

config = {
	'model_def' : './models/deploy.prototxt',
	# 'model_weights' : './models/model_icdar15.caffemodel',
	'model_weights': './models/VGGNet/text/text_polygon_precise_fix_order_384x384/VGG_text_text_polygon_precise_fix_order_384x384_iter_120000.caffemodel',
	'img_dir' : './demo_images/data/',
	'image_name' : 'test.jpg',
	'det_visu_path' : './demo_images/detection_result/',
	'det_save_dir' : './demo_images/detection_result/',
	'reco_save_dir' : './demo_images/recognition_result/',
	'crop_dir' : './demo_images/crops/',
	'input_height' : 384,
	'input_width' : 384,
	'overlap_threshold' : 0.1,
	'det_score_threshold' : 0.25,
	'visu_detection' : True,
}

net = caffe.Net(config['model_def'],	 # defines the structure of the model
			config['model_weights'],  # contains the trained weights
			caffe.TEST)     # use test mode (e.g., don't perform dropout)

def prepare_network(config):
	transformer = caffe.io.Transformer({'data': (1,3,config['input_height'], config['input_width'])})
	transformer.set_transpose('data', (2, 0, 1))
	transformer.set_mean('data', np.array([104,117,123])) # mean pixel
	# transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
	# transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

	net.blobs['data'].reshape(1,3,config['input_height'], config['input_width'])
	image = cv2.imread(os.path.join(config['img_dir'], config['image_name']))

	# # Resize small image with padding
	# sp = image.shape
	# HEIGHT = config['input_height']
	# WIDTH = config['input_width']
	# if sp[0] < HEIGHT or sp[1] < WIDTH:
	# 	top = int(max(HEIGHT - sp[0], 0) / 2)
	# 	bottom = int(max(HEIGHT - sp[0], 0) / 2)
	# 	left = int(max(WIDTH - sp[1], 0) / 2)
	# 	right = int(max(WIDTH - sp[1], 0) / 2)
	# 	image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT)

	# image=caffe.io.load_image(os.path.join(config['img_dir'], config['image_name']))
	transformed_image = transformer.preprocess('data', image)
	net.blobs['data'].data[...] = transformed_image
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# return net, image
	# return transformer, net
	return image

def extract_detections(detections, det_score_threshold, image_height, image_width):
	det_conf = detections[0,0,:,2]
	det_x1 = detections[0,0,:,7]
	det_y1 = detections[0,0,:,8]
	det_x2 = detections[0,0,:,9]
	det_y2 = detections[0,0,:,10]
	det_x3 = detections[0,0,:,11]
	det_y3 = detections[0,0,:,12]
	det_x4 = detections[0,0,:,13]
	det_y4 = detections[0,0,:,14]
	# Get detections with confidence higher than 0.6.
	top_indices = [i for i, conf in enumerate(det_conf) if conf >= det_score_threshold]
	top_conf = det_conf[top_indices]
	top_x1 = det_x1[top_indices]
	top_y1 = det_y1[top_indices]
	top_x2 = det_x2[top_indices]
	top_y2 = det_y2[top_indices]
	top_x3 = det_x3[top_indices]
	top_y3 = det_y3[top_indices]
	top_x4 = det_x4[top_indices]
	top_y4 = det_y4[top_indices]

	bboxes=[]
	for i in xrange(top_conf.shape[0]):
		x1 = int(round(top_x1[i] * image_width))
		y1 = int(round(top_y1[i] * image_height))
		x2 = int(round(top_x2[i] * image_width))
		y2 = int(round(top_y2[i] * image_height))
		x3 = int(round(top_x3[i] * image_width))
		y3 = int(round(top_y3[i] * image_height))
		x4 = int(round(top_x4[i] * image_width))
		y4 = int(round(top_y4[i] * image_height))
		x1 = max(1, min(x1, image_width - 1))
		x2 = max(1, min(x2, image_width - 1))
		x3 = max(1, min(x3, image_width - 1))
		x4 = max(1, min(x4, image_width - 1))
		y1 = max(1, min(y1, image_height - 1))
		y2 = max(1, min(y2, image_height - 1))
		y3 = max(1, min(y3, image_height - 1))
		y4 = max(1, min(y4, image_height - 1))
		score = top_conf[i]
		bbox=[x1,y1,x2,y2,x3,y3,x4,y4,score]
		bboxes.append(bbox)
	return bboxes

def apply_quad_nms(bboxes, overlap_threshold):
	dt_lines = sorted(bboxes, key=lambda x:-float(x[8]))
	nms_flag = nms(dt_lines, overlap_threshold)
	results=[]
	for k,dt in enumerate(dt_lines):
		if nms_flag[k]:
			if dt not in results:
				results.append(dt[:-1])
	return results

def save_and_visu(image, dt_results, reco_results, config):
	image_name = config['image_name']
	img_pil = Image.fromarray(image)
	draw = ImageDraw.Draw(img_pil)
	for i, result in enumerate(dt_results):
		draw.polygon(tuple(result), outline='red')
		draw.text(tuple(result[-2:]), reco_results[i], font=font, fill=(255, 0, 0))
	img_cv = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)
	cv2.imwrite(config['det_visu_path'] + image_name, img_cv)

def main():
	frd_time = 0
	nms_time = 0
	recog_time = 0
	total_time = 0

	# Select if multi-scale used
	use_multi_scale = False
	if not use_multi_scale:
		scales = ((384, 384),)
	else:
		# scales = ((300, 300), (700, 700), (700, 500), (700, 300), (1600, 1600))
		scales = ((384, 384), (640, 640))

	# Process folder files
	total_time_st = time.time()
	for files in os.walk(config['img_dir']):
		for file in files[2]:
			print(file + "-->start!")

			# Update detect results
			dt_results = []

			# Detect in all scales
			for scale in scales:
				print(scale)
				config['input_height'] = scale[0]
				config['input_width'] = scale[1]
				config['image_name'] = file
				image = prepare_network(config)
				image_height, image_width, channels = image.shape

				# Forward pass.
				tmp_time = time.time()
				detections = net.forward()['detection_out']
				frd_time += time.time() - tmp_time

				# Parse the outputs.
				bboxes = extract_detections(detections, config['det_score_threshold'], image_height, image_width)
				# dt_results.append(bboxes)
				dt_results.extend(bboxes)

			# Apply non-maximum suppression
			tmp_time = time.time()
			dt_nms_results = apply_quad_nms(dt_results, config['overlap_threshold'])
			nms_time += time.time() - tmp_time

			# Apply text recognition with crnn model
			tmp_time = time.time()
			reco_results = crnnRec(model, converter, image, dt_nms_results)
			recog_time += time.time() - tmp_time

			# Visualization and result saving
			save_and_visu(image, dt_nms_results, reco_results, config)

			# Text recognition result
			text_rec_res = {}
			text_rec_res["file_name"] = file
			text_rec_res["polygons"] = dt_nms_results
			text_rec_res["text"] = reco_results

			json_save_path = os.path.join(config['reco_save_dir'], file.split('.')[0] + '.json')
			with open(json_save_path, "w") as f:
				json.dump(text_rec_res, f)
	total_time = time.time() - total_time_st
	print('detection & recognition finished')
	print('Average forward time is: {}'.format(frd_time / 199))
	print('Average nms time is: {}'.format(nms_time / 199))
	print('Average recog time is: {}'.format(recog_time / 199))
	print('Total time is: {}'.format(total_time))

if __name__ == "__main__":
	main()
