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
        
        point_pixel = [(95, 403), (209, 248), (547, 403), (437, 248)]
        point_real = [(-15, 12.5), (-15, 33.5), (15, 12.5), (15, 33.5)]
        
        self.perspective = Perspective(image, point_pixel, point_real)


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
    

    def read_cam(self) -> np.ndarray:
        img_read = self.picam.capture_array()
        
        img_calibration = self.calibraion(img_read)
        
        self.img_width, self.img_height = img_calibration.shape[1], img_calibration.shape[0]
        
        center = (self.img_width // 2, self.img_height // 2)

        angle = 0.75
        scale = 1.0
        M = cv2.getRotationMatrix2D(center, angle, scale)

        image_warp = cv2.warpAffine(img_calibration, M, (self.img_width, self.img_height)) 

        image_cropp = image_warp[0:1900, 380:2280,:3]

        img_resize = cv2.resize(image_cropp, (self.width_out, self.height_out), interpolation = cv2.INTER_AREA)
        
        self.image_out = cv2.cvtColor(img_resize, cv2.COLOR_RGB2BGR)

        self.img_width, self.img_height = self.image_out.shape[1], self.image_out.shape[0]

        # print('Camera read')
        # print(type(image_out), self.img_width, self.img_height)

        # cv2.imwrite('test.png',image_out)
        
        return self.image_out
    