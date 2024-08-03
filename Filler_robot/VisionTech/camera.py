import cv2
import numpy as np
import math
from picamera2 import Picamera2
import logging

#from Lib.Decorators.wrapper import _timing
from Filler_robot.VisionTech.perspective import Perspective


class Camera:
    def __init__(self):
        self.print_on = True

        logging.debug("Initializing camera...")
        try:
            self.picam = Picamera2()
            logging.debug("Camera initialized successfully.")
        except RuntimeError as e:
            logging.error(f"Failed to initialize camera: {e}")
            raise

        config = self.picam.create_still_configuration(main={"size": (2592, 1944)})
        self.picam.configure(config)

        self.cv_file = cv2.FileStorage('Filler_robot/VisionTech/calibration/camera_params.yml', cv2.FILE_STORAGE_READ)
        self.camera_matrix = self.cv_file.getNode('K').mat()
        self.distortion_coeffs = self.cv_file.getNode('D').mat()
        self.cv_file.release()

        self.calibration_on = True
        
        print(self.camera_matrix, self.distortion_coeffs)
        
        self.picam.start()
        
        self.img = []
        
        self.img_width = 640
        self.img_height = 640
        
        self.width_out = 640
        self.height_out = 640

        image = np.zeros((self.width_out, self.height_out, 3), dtype=np.uint8)
        
        point_pixel = [(30, 430), (221, 214), (610, 430), (419, 214)]
        point_real = [(-20, 11.2), (-20, 50.7), (20, 11.2), (20, 50.7)]
        
        self.perspective = Perspective(image, point_pixel, point_real)


    #@_timing(True)
    def running(self):
        self.read_cam()
    
    
    def stop(self):    
        self.picam.close()
        self.picam.stop()

    
    def calibraion(self, image):
        image = cv2.undistort(image , self.camera_matrix, self.distortion_coeffs)
        #image = cv2.fisheye.undistortImage(image, self.camera_matrix, self.distortion_coeffs)
        #image = image[:, 124:2468,:3]

        return image
    

    #@_timing(True)
    def read_cam(self) -> np.ndarray:
        self.img = self.picam.capture_array()
        
        if self.calibration_on:
            self.img = self.calibraion(self.img)
        
        self.img_width, self.img_height = self.img.shape[1], self.img.shape[0]
        
        center = (self.img_width // 2, self.img_height // 2)

        angle = 0.75
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle, scale)

        self.img = cv2.warpAffine(self.img, M, (self.img_width, self.img_height))
        
        #self.img = self.img[0:1900, 300:2200,:3]
        self.img = self.img[0:1900, 380:2280,:3]
        #self.img = self.img[:, :,:3]

        self.img_monitor = self.img.copy()

        self.img = cv2.resize(self.img, (self.width_out, self.height_out), interpolation = cv2.INTER_AREA)
        
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        
        self.img_width, self.img_height = self.img.shape[1], self.img.shape[0]
       
        if self.print_on:
            print('Camera read')
            
        print(type(self.img), self.img_width, self.img_height)

        #cv2.imwrite('test.png', self.img)
        
        return self.img
    

# camera = Camera()

# while True:
#     camera.read_cam()
