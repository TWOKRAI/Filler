from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

from Gadgets.VisionTech.camera import camera
from Filler_robot.NeuroModules.neuron import neuron
from Filler_robot.NeuroModules.interface import interface
from Filler_robot.Robots.robot_module import robot

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot(QThread):
    frame_captured = pyqtSignal(np.ndarray)

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
            if self.camera_on: camera.run()
            if self.neuron_on: neuron.run()

            temp = check_temperature()
            write_to_file(temp, 'log_temp.txt')

            if self.inteface_on: 
                interface.run()
            else:
                image = interface.save_image()

                if isinstance(image, np.ndarray):
                    self.frame_captured.emit(image)

            if self.robot_on: robot.run()

            QThread.msleep(2000)


robot = Robot()

