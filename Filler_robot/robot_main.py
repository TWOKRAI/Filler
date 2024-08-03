from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QPixmap
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
# from Filler_robot.Robots.robot_module import robot

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot_filler(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.running = True

        self.camera = Camera()
        self.neuron = Neuron()
        self.interface = Interface()

        self.camera_on = True
        self.robot_on = False
        self.inteface_on = False
        self.neuron_on = True
        
        clear_file('log_temp.txt')


    def stop(self):
        self.running = False
    

    def run(self) -> None:
        self.image_cam = None

        while self.running:
            # temp = check_temperature()
            # write_to_file(temp, 'log_temp.txt')
            
            self.image_cam = self.camera.read_cam()

            if self.image_cam is not None and isinstance(self.image_cam, np.ndarray):
                objects_list = self.neuron.find_objects(self.image_cam)
                self.interface.save_image(self.image_cam, objects_list)
                QThread.msleep(300)
                self.image_cam = None

            # if self.robot_on: 
            #     robot.running()
            # else:
            #     robot.enable_motors(False)

            #QThread.msleep(1000)

        self.camera.stop()


    # @pyqtSlot(bool)
    def enable_neuron_on(self, value = False):
        if value:
            self.neuron_on = True
        else:
            self.neuron_on = False
    
    
    # @pyqtSlot(bool)
    def enable_robot_on(self, value = False):
        if value:
            self.robot_on = True
        else:
            self.robot_on = False


