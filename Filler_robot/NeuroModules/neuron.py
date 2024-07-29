import cv2
import numpy as np
import time
import math

from Gadgets.VisionTech.camera import camera

from Lib.Decorators.wrapper import _timing


file = open("Filler_robot/NeuroModules/models/coco.txt","r")
classes = file.read().split('\n')
#print(classes)

classes_file = 'Filler_robot/NeuroModules/models/coco.names'
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
	def __init__(self):
		self.timer = Timer()

		self.net_v5 = cv2.dnn.readNetFromONNX("Filler_robot/NeuroModules/models/yolov5s.onnx")
		self.net_v5.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		self.net_v5.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
		
		self.mode = 0
		
		self.threshold = 0.5
		
		self.nmsthreshold = 0.5

		self.list_find = {'cup': True, 'CUP': True, 'vase': True, 'wine glass': True, 'toilet': True, 'person': True}
		
		self.position = 0
		self.next_position_0 = True
		self.next_position_1 = False
		self.next_position_2 = False
		self.next_position_list = []
		
		self.limit_xmin = 30
		self.limit_xmax = camera.img_width - 50
		self.limit_ymin = 0
		self.limit_ymax = 300
		
		self.factor_x = 10
		self.factor_y = 0.1
		self.perspective = 0

		self.objects_all = []
        
		self.memory_objects = []
		self.objects = []
			
		self.list_coord = []
		
		self.region_x = 20
		self.region_y = 20
		self.leen = 1800
		
		self.hands_data = []
		self.hands_found = False
   

	@_timing(True)
	def run(self):
		if self.timer.is_time_passed(5):
			self.find_objects()
			self.find_objects()


	def find_objects(self):
		self.objects = self.detect_v5(camera.img)
			
		self.objects = self.filter()
		
		self.list_coord = self.pixel_to_coord(self.objects)
	

	@_timing(True)
	def detect_v5(self, image):
		self.objects_all = []

		if type(image) is np.ndarray:
				x_scale = camera.img_width/640
				y_scale = camera.img_height/640
				
				blob = cv2.dnn.blobFromImage(image, scalefactor= 1/255, size=(640, 640), mean=[0,0,0], swapRB= True, crop= False)
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
							x1 = int((cx- w/2)*x_scale)
							y1 = int((cy-h/2)*y_scale)
							width = int(w * x_scale)
							height = int(h * y_scale)
							box = np.array([x1,y1,width,height])
							boxes.append(box)
							
				indices = cv2.dnn.NMSBoxes(boxes,confidences,self.threshold, self.nmsthreshold)

				for i in indices:
					id_obj = 0
					ready = False
					
					x1,y1,w,h = boxes[i]
					label = classes[classes_ids[i]]
					conf = confidences[i]
					
					yr_center = int(y1 + w*(y1+h)/self.leen)
					xr_center = int(x1 + w/2)

					self.perspective = (xr_center - camera.img_width/2) * 1/self.factor_x

					yr_center_2 = int(y1 + h - w*(y1+h)/self.leen * 1.5)
					xr_center_2 = int(x1 + w/2) - self.perspective		
					
					print('perspective', self.perspective)
					
					xr_center = int(xr_center + self.perspective)
					
					self.objects_all.append([ready, id_obj, label, conf, x1, y1, w, h, xr_center, yr_center, self.perspective, xr_center_2, yr_center_2])
					print('self.objects', self.objects)
					
				print('1 objects', self.objects_all)

		return self.objects_all
	
		
	@_timing(True)
	def filter(self):
		objects_new = []
		
		objects = sorted(self.objects, key = lambda sublist: sublist[4])
			
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
						
		print('3 Filter  self.objects:', objects)

		return objects
	

	def pixel_to_coord(self, objects):
		list_coord = []
		
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

			x = xr_center_2
			
			if abs(camera.img_width/2  - xr_center_2) < 9:
				y = yr_center_2 - (camera.img_height - (y1 + h)) ** 2 * 0.00031 + math.sqrt(abs(camera.img_width/2  - xr_center_2)) * 0.01
			else:
				y = yr_center_2 + 1

			
			#ssinput()
			z = h * 0.004 * math.sqrt(camera.img_height - (y1 + h)) + (camera.img_height - (y1 + h)) ** 2 * 0.00007 - abs(camera.img_width/2  - xr_center_2) * 0.004


			point = (x, y)
			
			point = camera.perspective.transform_coord(point)
			point = camera.perspective.scale(point)

			x = round(point[0], 1)
			y = round(point[1], 1)
			z = round(z, 1)
			
			list_coord.append((x, y, z))
			
			print('w', w)
		
		print('list_coord', list_coord)
		
		#input('PIXXXEL')
		
		return list_coord
		

neuron = Neuron()
