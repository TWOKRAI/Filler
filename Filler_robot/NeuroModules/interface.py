import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


from Lib.Decorators.wrapper import _timing

import numpy as np


def nothing(x):
	pass


class Interface(QObject):
	frame_captured = pyqtSignal(QPixmap)

	def __init__(self, camera, neuron):
		super().__init__()

		self.camera = camera
		self.neuron = neuron

		self.visual = True

		self.x = 0
		self.y = 0

		self.img_monitor = None
		
		# self.create_window()


	def _visual_line(func):
		def wrapper(*args):
			self = args[0]
			
			if self.visual == True:
				func(*args)
			
		return wrapper	
	
	
	# @_timing(True)	
	def running(self):
		self.save_image()
		# self.get_trackbar()

	
	def create_window(self):
		cv2.namedWindow( "Detect" )
		cv2.createTrackbar("x_point", "Detect" , 320, self.camera.img_width, nothing)
		cv2.createTrackbar("y_point", "Detect" , 360, self.camera.img_height, nothing) #371

		self.get_trackbar()

  		
	def get_trackbar(self):
		self.x = cv2.getTrackbarPos("x_point", "Detect")
		self.y = cv2.getTrackbarPos("y_point", "Detect")


	# @_timing(True)			
	def show_img(self, image):
		img_copy = image.img.copy()
		
		# self.draw_sight(img_copy)
		# self.draw_limit_line(img_copy)
		# self.draw_box_all(img_copy)
		self.draw_box(img_copy)
		# self.perspective(img_copy)

		# point = (self.x, self.y)
		# point = camera.perspective.transform_coord(point)

		# point = camera.perspective.scale(point)

		# camera.perspective.draw(img_copy)
		
		cv2.imshow("Detect", img_copy)
		cv2.waitKey(1)
		
		print('image_show')
		
	
	def destroy_window(self):
		cv2.destroyAllWindows()

	
	def save_image(self):
		if isinstance(self.camera.image_out, np.ndarray):
			image_draw = self.draw_box(self.camera.image_out, self.neuron.objects_filter)

			self.draw_box_all(image_draw)

			point = (self.x, self.y)
			point = self.camera.perspective.transform_coord(point)

			point = self.camera.perspective.scale(point)

			# self.camera.perspective.draw(image_draw)

			img_monitor = image_draw[60:430,:]

			h, w, ch = img_monitor.shape
			
			q_image = QImage(img_monitor.data.tobytes(), w, h, ch * w, QImage.Format_BGR888)
			q_image = q_image.scaled(720, 480, Qt.KeepAspectRatio)

			pixmap = QPixmap.fromImage(q_image)

			self.frame_captured.emit(pixmap)

			print(self.camera.image_out.shape)
			

		# self.img_monitor = camera.img_monitor[100:1700, 380:2280,:3]

		# self.img_monitor = cv2.resize(self.img_monitor, (720, 480), interpolation = cv2.INTER_AREA)

		# self.draw_box_all(self.img_monitor)
		# self.draw_box(self.img_monitor)
		# self.perspective(self.img_monitor)

		
	
	# @_visual_line
	# def draw_sight(self, img):
	# 	size = 300
	
	# 	# cv2.line(img, (int(camera.img_width/2), int(camera.img_height/2) - size), (int(camera.img_width/2 ) , int(camera.img_height/2) + size), (0, 0, 0), 2)
	# 	# cv2.line(img, (int(camera.img_width/2) - size, int(camera.img_height/2)), (int(camera.img_width/2) + size, int(camera.img_height/2)), (0, 0, 0), 2)
		
	# 	cv2.line(img, (int(camera.img_width/2), int(camera.img_height/2) - size), (int(camera.img_width/2 ) , int(camera.img_height/2) + size), (0, 0, 0), 2)
	# 	cv2.line(img, (int(camera.img_width/2) - size, int(camera.img_height/2)), (int(camera.img_width/2) + size, int(camera.img_height/2)), (0, 0, 0), 2)


	# def perspective(self, img):
	# 	cv2.circle(img, (self.x, self.y), 5, (255, 0, 255), -1)
		

	# @_visual_line
	# def draw_limit_line(self, img):
	# 	cv2.line(img, (neuron.limit_xmin, 0), (neuron.limit_xmin, camera.img_height), (255, 0, 0), 1)
	# 	cv2.line(img, (neuron.limit_xmax, 0), (neuron.limit_xmax, camera.img_height), (255, 0, 0), 1)
		
	# 	cv2.line(img, (0, neuron.limit_ymax), (camera.img_width, neuron.limit_ymax), (255, 0, 0), 1)

		
	def draw_box(self, image, objects):
		i = 0

		if objects != None:
			for obj in objects:
				ready = obj[0]
				id_obj = obj[1]
				label = obj[2]
				conf = obj[3]
				x1 = obj[4]
				y1 = obj[5]
				w = obj[6]
				h = obj[7]
				xr_center = obj[8]
				yr_center = obj[9]
				perspective = obj[10]
				xr_center_2 = obj[11]
				yr_center_2 = obj[12]
				
				if ready == False:
					color_box = (255, 0, 0)
				else:
					color_box = (0, 0, 255)	

				#print('wfwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', camera.perspective_transformed([neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10]), neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10)

				text = f'{id_obj}' + ':' + label + ' ' + f'{ready}'
				cv2.rectangle(image,(x1, y1),(x1 + w, y1 + h), color_box, 2)
				cv2.putText(image, text, (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, color_box, 1)

				cv2.rectangle(image, (int(xr_center - 4), yr_center - 4),(int(xr_center + 4), yr_center + 4), (255, 255, 0), -1)
				cv2.rectangle(image, (int(xr_center - self.neuron.region_x), yr_center - self.neuron.region_y),(int(xr_center + self.neuron.region_x), yr_center + self.neuron.region_y), (0, 255, 0), 1)
				
				cv2.rectangle(image, (int(xr_center_2 - 4), yr_center_2 - 4),(int(xr_center_2 + 4), yr_center_2 + 4), (255, 255, 0), -1)

				cv2.putText(image, f'{self.neuron.list_coord[i]}', (x1 - 20, y1 - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)

				cv2.line(image, (x1, yr_center), (x1 + w, yr_center), (255, 255, 0), 1)
				
				# cv2.line(image, (int(xr_center), yr_center), (int(xr_center - perspective * 4), y1 + h), (255, 255, 0), 1)

				cv2.line(image, (int(xr_center), yr_center), (int(xr_center_2), yr_center_2), (255, 255, 0), 1)

				i += 1
		
		return image


	def draw_box_all(self, img):
		objects = self.neuron.objects_all

		i = 0
		
		for obj in objects:
			ready = obj[0]
			id_obj = obj[1]
			label = obj[2]
			conf = obj[3]
			x1 = obj[4]
			y1 = obj[5]
			w = obj[6]
			h = obj[7]
			xr_center = obj[8]
			yr_center = obj[9]
			perspective = obj[10]
			xr_center_2 = obj[11]
			yr_center_2 = obj[12]
			
			label_person = 'PERSON'
				
			color_box = (0, 255, 0)	
			color_text = (0, 90, 0)	

			#print('wfwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww', camera.perspective_transformed([neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10]), neuron.list_coord[i][0] * 10, neuron.list_coord[i][1] * 10)

			if label == 'cocperson':
				cv2.rectangle(img,(x1, y1),(x1 + w, y1 + h), color_box, 2)
				cv2.putText(img, f'{label_person}', (x1, y1 - 2), cv2.FONT_HERSHEY_COMPLEX, 0.7, color_text, 1)

			#cv2.rectangle(img, (int(xr_center - 4), yr_center - 4),(int(xr_center + 4), yr_center + 4), (255, 255, 0), -1)
			#cv2.rectangle(img, (int(xr_center - neuron.region_x), yr_center - neuron.region_y),(int(xr_center + neuron.region_x), yr_center + neuron.region_y), (0, 255, 0), 1)
			
			#cv2.rectangle(img, (int(xr_center_2 - 4), yr_center_2 - 4),(int(xr_center_2 + 4), yr_center_2 + 4), (255, 255, 0), -1)

			#cv2.putText(img, f'{neuron.list_coord[i]}', (x1 - 20, y1 - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 0), 1)

			#cv2.line(img, (x1, yr_center), (x1 + w, yr_center), (255, 255, 0), 1)
			
			#cv2.line(img, (int(xr_center), yr_center), (int(xr_center - perspective * 4), y1 + h), (255, 255, 0), 1)

			#cv2.line(img, (int(xr_center), yr_center), (int(xr_center_2), yr_center_2), (255, 255, 0), 1)

			#i += 1
			
# interface = Interface()
