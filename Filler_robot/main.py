from PyQt5.QtCore import QThread

from Gadgets.VisionTech.camera import camera
from NeuroModules.neuron import neuron
from NeuroModules.interface import interface
from Robots.robot_module import robot


class Filler(QThread):
    def __init__(self) -> None:
        self.running = True

        self.camera_on = True
        self.robot_on = False
        self.inteface_on = True
        self.neuron_on = True

    def stop(self):
        self.running = False
    
    def run(self) -> None:
        while self.running:
            if self.camera_on: camera.run()
            if self.neuron_on: neuron.run() 
            if self.inteface_on: interface.run()
            if self.robot_on: robot.run()


if __name__ == '__main__':
    filler = Filler()
    filler.start()
