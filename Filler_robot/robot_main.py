from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.Robots.robot_module import Robot_module

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot_filler(QObject):
    def __init__(self, robot_on = False) -> None:
        super().__init__()

        self.running = True

        self.camera = Camera()
        self.neuron = Neuron(self.camera)
        self.interface = Interface(self.camera, self.neuron)
        self.robot = Robot_module(self.camera, self.neuron, self.interface)

        self.camera_on = True
        self.neuron_on = False
        self.inteface_on = True
        self.robot_on = robot_on
        
        clear_file('log_temp.txt')


    def stop(self):
        self.running = False
    

    def run(self) -> None:
        while self.running:
            # temp = check_temperature()
            # write_to_file(temp, 'log_temp.txt')
            
            if self.camera_on: self.camera.running()
            if self.neuron_on: self.neuron.find_objects()
            if self.inteface_on: self.interface.running()
            if self.robot_on: self.robot.running()

            
            #QThread.msleep(300)

            # if image_cam is not None and isinstance(image_cam, np.ndarray):
            #     self.neuron.find_objects(image_cam)

            #     self.interface.save_image(image_cam)
                
            #     image_cam = None
            # else:
            #     QThread.msleep(300)

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


