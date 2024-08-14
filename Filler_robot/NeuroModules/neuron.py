import cv2
import numpy as np
import time
import math
import os
import time

from Filler_robot.VisionTech.camera import Camera

from Lib.Decorators.wrapper import _timing


file_path = os.path.join('/home/innotech/Project/Filler/Filler_robot/NeuroModules/models', 'coco.txt')
file = open(file_path,"r")
# file = open("Filler_robot/NeuroModules/models/coco.txt","r")
classes = file.read().split('\n')
#print(classes)

file_path = os.path.join('/home/innotech/Project/Filler/Filler_robot/NeuroModules/models', 'coco.names')
classes_file = file_path
# classes_file = 'Filler_robot/NeuroModules/models/coco.names'
class_names = []

with open(classes_file, 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')      


class Timer:
	def __init__(self):
		self.start_time = 0


	def start(self):
		self.start_time = time.time()	


	def is_time_passed(self, seconds):
		current_time = time.time()
		elapsed_time = current_time - self.start_time

		return elapsed_time >= seconds
	

class Neuron:
	def __init__(self, camera):
		self.camera = camera

		self.timer = Timer()

		# file_path1 = os.path.join('Filler_robot', 'NeuroModules', 'models', 'yolov4-tiny.cfg')
		# file_path2 = os.path.join('Filler_robot', 'NeuroModules', 'models', 'yolov4-tiny.weights')
		# self.net_v4 = cv2.dnn.readNetFromDarknet(file_path1, file_path2)
		# self.net_v4.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		# self.net_v4.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


		file_path = os.path.join('/home/innotech/Project/Filler/Filler_robot/NeuroModules/models', 'yolov5n.onnx')
		self.net_v5 = cv2.dnn.readNetFromONNX(file_path)
		# self.net_v5.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		# self.net_v5.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
		
		self.mode = 0
		
		self.threshold = 0.4
		self.nmsthreshold = 0.4

		self.list_find = {'cup': True, 'CUP': True, 'vase': True, 'wine glass': True, 'toilet': True, 'person': True}
		
		self.position = 0
		self.next_position_0 = True
		self.next_position_1 = False
		self.next_position_2 = False
		self.next_position_list = []
		
		self.limit_xmin = 30
		self.limit_xmax = 640 - 50
		self.limit_ymin = 0
		self.limit_ymax = 300
		
		self.factor_x = 12
		self.factor_y = 0.1
		self.perspective = 0

		self.objects_all = []
        
		self.memory_objects = []
		self.objects = []
			
		self.list_coord = []

		self.objects_filter = []
		
		self.region_x = 15
		self.region_y = 15
		self.leen = 1800
		
		self.hands_data = []
		self.hands_found = False
   

	def running(self):
		if self.timer.is_time_passed(5):
			self.find_objects()
			self.find_objects()
			self.find_objects()


	def find_objects(self):
		objects_list = self.detect_v5(self.camera.image_out)
		self.objects_filter = self.filter(objects_list)

		self.list_coord = self.pixel_to_coord(self.objects_filter)

	
	def detect_v5(self, image):
		self.objects_all = []

		if isinstance(image, np.ndarray):
			img_width, img_height = image.shape[1], image.shape[0]

			x_scale = img_width / 640
			y_scale = img_height / 640

			blob = cv2.dnn.blobFromImage(image, scalefactor=1/255, size=(640, 640), mean=[0, 0, 0], swapRB=True, crop=False)
			self.net_v5.setInput(blob)
			detections = self.net_v5.forward()[0]

			classes_ids = []
			confidences = []
			boxes = []
			rows = detections.shape[0]

			for i in range(rows):
				row = detections[i]
				confidence = row[4]
				if confidence > self.threshold:
					classes_score = row[5:]
					ind = np.argmax(classes_score)
					if classes_score[ind] > 0.5:
						classes_ids.append(ind)
						confidences.append(confidence)
						cx, cy, w, h = row[:4]
						x1 = int((cx - w / 2) * x_scale)
						y1 = int((cy - h / 2) * y_scale)
						width = int(w * x_scale)
						height = int(h * y_scale)
						box = np.array([x1, y1, width, height])
						boxes.append(box)

			indices = cv2.dnn.NMSBoxes(boxes, confidences, self.threshold, self.nmsthreshold)

			if isinstance(indices, np.ndarray):
				for i in indices:
					id_obj = 0
					ready = False

					x1, y1, w, h = boxes[i]
					label = classes[classes_ids[i]]
					conf = confidences[i]

					yr_center = int(y1 + w * (y1 + h) / self.leen)
					xr_center = int(x1 + w / 2)

					self.perspective = (xr_center - img_width / 2) * 1 / self.factor_x

					print('H', h)

					if h <= 190:
						xd = 0  
						yd = 0
					else:
						xd = 10 
						yd = 10

					
					# xr_center_2 = int(x1 + w / 1.8) - self.perspective * 1.2

					
					# yr_center_2 = int((y1 + h1) - h1 * 0.3) 
					
					if xr_center >= self.camera.img_width / 2:
						xr_center_2 = int((xr_center - self.perspective * 2)) - xd #+ (w * 0.165) * abs(self.camera.img_width / 2 - xr_center) / 320) * 0.97
					else:
						xr_center_2 = int((xr_center - self.perspective * 2)) + xd #- (w * 0.165) * abs(self.camera.img_width / 2 - xr_center) / 320) * 0.97

					
					yr_center_2 = int(((y1 + h) - w / 2 * 0.7) + (1 - abs(self.camera.img_height - (y1 + h)) / 700)) + yd

					yr_center = int((y1 + w / 2 * 0.5 * (1 + h/1000)))
					xr_center = int(xr_center + self.perspective)

					self.objects_all.append([ready, id_obj, label, conf, x1, y1, w, h, xr_center, yr_center, self.perspective, xr_center_2, yr_center_2])
			else:
				self.objects_all = []

		return self.objects_all
	

	def detect_v4(self, image):
		self.objects_all = []

		# image = cv2.resize(image, (320, 320), interpolation = cv2.INTER_AREA)
		
		blob = cv2.dnn.blobFromImage(image, 1/255, (320, 320), [0,0,0], 1, crop = True)
		self.net_v4.setInput(blob)
		detections = self.net_v4.forward()[0]
		
		layers_names = self.net_v4.getLayerNames()
		#print(net.getUnconnectedOutLayers())
		output_names = [layers_names[i-1] for i in self.net_v4.getUnconnectedOutLayers()]
		outputs = self.net_v4.forward(output_names)
		
		ht, wt, ct = image.shape
		bbox = []
		classIds = []
		confs = []
		
		for output in outputs:
			for det in output:
				scores = det[5:]
				classId = np.argmax(scores)
				confidence = scores[classId]
				if confidence > self.threshold:
					w, h = int(det[2]*wt), int(det[3]*ht)
					x, y = int((det[0]*wt) - w/2), int((det[1]*ht) - h/2)
					bbox.append([x,y,w,h])
					classIds.append(classId)
					confs.append(float(confidence))
		
		indices = cv2.dnn.NMSBoxes(bbox, confs, self.threshold, self.nmsthreshold)
		
		for i in indices:
			id_obj = 0
			ready = False
			label = class_names[classIds[i]].upper()
			conf = int(confs[i]*100) 
			box = bbox[i]
			x1, y1, w, h = box[0], box[1], box[2], box[3]
			
			yr_center = int(y1 + w*(y1 + h * 1.2)/self.leen)
			xr_center = int(x1 + w/2)
					
			self.perspective = (xr_center - wt/2) * 1/ self.factor_x
			
			print('perspective', self.perspective)
			
			xr_center = int(xr_center + self.perspective)

			# if y1 >= 300:

			
			self.objects_all.append([ready, id_obj, label, conf, x1, y1, w, h, xr_center, yr_center, self.perspective])
			print('objects', self.objects_all)
			

		print('1 self.all_objects', self.objects_all)

		return self.objects_all


	def filter(self, objects_list):
		objects_new = []
		
		objects = sorted(objects_list, key = lambda sublist: sublist[4])
			
		find = False
		
		for obj in objects:
			label = obj[2]
			
			xr_center = obj[8]
			yr_center = obj[9]

			find = self.list_find.get(label, False)
			
			if find == True:
				should_add = True
			
				for prev_obj in self.memory_objects:
					prev_status = prev_obj[0]
					prev_xr_center = prev_obj[8]
					prev_yr_center = prev_obj[9]

					if abs(xr_center - prev_xr_center) <= self.region_x and abs(yr_center - prev_yr_center) <= self.region_y:
						if prev_status == True:
							obj[0] = True
							should_add = False
						else:
							obj[0] = False
							
						break 
								
				if should_add == True:
					objects_new.append(obj) 
				else:
					objects_new.append(prev_obj)
					
		objects_new = sorted(objects_new, key = lambda sublist: sublist[4])			

		id_objects = []
		id_obj = 1
		
		for obj in objects_new:
			obj[1] = id_obj
			id_obj += 1
			id_objects.append(obj)

		objects = id_objects
						
		# print('3 Filter  self.objects:', objects)

		return objects
	

	def pixel_to_coord(self, objects):
		list_coord = []

		img_width, img_height = self.camera.img_width , self.camera.img_height

		for obj in objects:
			x1 = obj[4]
			y1 = obj[5]
			w = obj[6]
			h = obj[7]
			xr_center = obj[8]
			yr_center = obj[9]	
			perspective = obj[10]
			xr_center_2 = obj[11]
			yr_center_2 = obj[12]

			x = x1
			y = y1
			z = h
			

			
			
			# if xr_center_2 < camera.img_width/2:
			# 	x = xr_center_2 * 1
			# else:
			# 	x = xr_center_2 * 1

			# if abs(camera.img_width/2  - xr_center_2) > 150:
			# 	if xr_center_2 < camera.img_width/2:
			# 		x = xr_center_2 + 40
			# 	else:
			# 		x = xr_center_2 - 40
			# else:
			# 	x = xr_center_2

			# x = xr_center_2
			
			# if abs(img_width/2  - xr_center_2) < 9:
			# 	y = yr_center_2 - (img_height - (y1 + h)) ** 2 * 0.00031 + math.sqrt(abs(img_width/2  - xr_center_2)) * 0.01
			# else:
			# 	y = yr_center_2 + 1

			
			# #ssinput()
			# z = h * 0.004 * math.sqrt(img_height - (y1 + h)) + (img_height - (y1 + h)) ** 2 * 0.00007 - abs(img_width/2  - xr_center_2) * 0.004

			x = xr_center_2
			y = yr_center_2

			z = h * 0.05 * (1 + (abs(self.camera.img_height - yr_center_2 - 150)/130)**3) * (1 - abs(self.camera.img_width/2 - xr_center_2)/1300)
			#z = h * 0.046 * (1 + abs(self.camera.img_height - yr_center_2)/500)
			# if z > 12:
			# 	z += 2


			# v = v * 0.00034

			# print('v', v)


			point = (x, y)
			point = self.camera.perspective.transform_coord(point)
			point = self.camera.perspective.scale(point)

			point_1 = (x1, y1 + h)
			point_1 = self.camera.perspective.transform_coord(point_1)
			point_1 = self.camera.perspective.scale(point_1)

			point_2 = (x1 + w, y1 + h)
			point_2 = self.camera.perspective.transform_coord(point_2)
			point_2 = self.camera.perspective.scale(point_2)


			dx = abs(point_1[0] - point_2[0])

			v = (dx / 2) ** 2 * z * 1.2

			print('VVV', v)
			

			x = round(point[0], 1)
			y = round(point[1], 1)
			z = round(z, 1)

			
			list_coord.append((x, y, z))
			
		# 	print('w', w)
		
		# print('list_coord', list_coord)
		
		#input('PIXXXEL')
		
		return list_coord
		

# neuron = Neuron()
