from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
import numpy as np

from Filler_robot.VisionTech.camera import camera
from Filler_robot.NeuroModules.neuron import neuron
from Filler_robot.NeuroModules.interface import interface
from Filler_robot.Robots.robot_module import robot

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot(QThread):
    def __init__(self) -> None:
        super().__init__()

        self.running = True

        self.camera_on = True
        self.robot_on = False
        self.inteface_on = False
        self.neuron_on = False
        
        clear_file('log_temp.txt')


    def stop(self):
        self.running = False
    

    def run(self) -> None:
        while self.running:
            temp = check_temperature()
            write_to_file(temp, 'log_temp.txt')
        
            if self.camera_on: camera.running()
            if self.neuron_on: neuron.running()
            #if self.neuron_on: self.whilet()

            if self.inteface_on: 
                interface.run()
            else:
                interface.save_image()

            if self.robot_on: 
                robot.running()
            else:
                robot.enable_motors(False)

            QThread.msleep(1000)


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


robot_filler = Robot()

