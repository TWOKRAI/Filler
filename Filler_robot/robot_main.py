from PyQt5.QtCore import QThread

from Gadgets.VisionTech.camera import camera
from Filler_robot.NeuroModules.neuron import neuron
from Filler_robot.NeuroModules.interface import interface
from Filler_robot.Robots.robot_module import robot


class Robot(QThread):
    def __init__(self) -> None:
        super().__init__()

        self.running = True

        self.camera_on = True
        self.robot_on = False
        self.inteface_on = False
        self.neuron_on = True

    def stop(self):
        self.running = False
    
    def run(self) -> None:
        while self.running:
            if self.camera_on: camera.run()
            if self.neuron_on: neuron.run() 
            if self.inteface_on: interface.run()
            interface.save_image()
            if self.robot_on: robot.run()


robot = Robot()

