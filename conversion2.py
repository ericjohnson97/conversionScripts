import json
import os
from os import walk, getcwd


def get_category_name(json_object, category_id):
    for dict in json_object:
        if dict['id'] == category_id:
            return dict['name']

def get_image_width(json_object, image_id):
	for dict in json_object:
		if dict['id'] == image_id:
			return dict['width']

def get_image_height(json_object, image_id):
	for dict in json_object:
		if dict['id'] == image_id:
			return dict['height']

def get_image_path(json_object, image_id):
	for dict in json_object:
			if dict['id'] == image_id:
				return dict['path']


def convert(size, box):
	dw = 1./size[0]
	dh = 1./size[1]
	x = (box[0] + box[1])/2.0
	y = (box[2] + box[3])/2.0
	w = box[1] - box[0]
	h = box[3] - box[2]
	x = x*dw
	w = w*dw
	y = y*dh
	h = h*dh
	return (x,y,w,h)






classes = ["Cargo"]

# Create lists.txt 
wd = getcwd()
list_file = open('%s/list.txt'%wd, 'w')	
local_path_list = []

with open('2019Cargo-1.json') as json_file:
	data = json.load(json_file)
	images = data['images']
	annotation_data = data['annotations']

	#index through annotations
	for i in range(len(data['annotations'])):

		image_id = annotation_data[i]['image_id']
		category_id = annotation_data[i]['category_id']
		object_class = get_category_name(data['categories'],category_id)
		xmin = annotation_data[i]['bbox'][0]
		ymin = annotation_data[i]['bbox'][1]
		xmax = xmin + annotation_data[i]['bbox'][2]
		ymax = ymin + annotation_data[i]['bbox'][3]
		
		print(xmin, ymin, xmax, ymax)

		#look up image metadata 
		w= get_image_width(images, image_id)
		h= get_image_height(images, image_id)
		path = get_image_path(images, image_id)
		local_path = path.split('/datasets/')[1]
		

		if local_path not in local_path_list:
			local_path_list.append(local_path) 
	
		
		### Create output text files 
		txt_outpath = os.path.splitext(local_path)[0] + ".txt"
		print("Output: " + txt_outpath)

		if os.path.exists(str(txt_outpath)):
			txt_outfile = open(txt_outpath, "a")  		
		else:
			txt_outfile = open(txt_outpath, "w")  		
	    
		b = (float(xmin), float(xmax), float(ymin), float(ymax))
		bb = convert((w,h), b)
		print(bb)

		cls_id = classes.index(str(object_class))
		txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
		txt_outfile.close()

for image_path in local_path_list:
	list_file.write(image_path+"\n")

list_file.close()
