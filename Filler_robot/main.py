from PyQt5.QtCore import QThread

from camera import camera 
from neuron import neuron
from interface import interface
from robot import robot


class Filler(QThread):
    def __init__(self) -> None:
        self.running = True

        self.camera_on = True
        self.robot_on = False
        self.inteface_on = True
        self.neuron_on = True

    
    def run(self) -> None:
        # if self.robot_on: robot.go_home()

        while self.running:
            if self.camera_on: camera.run()
            if self.neuron_on: neuron.run() 
            if self.inteface_on: interface.run()
            if self.robot_on: robot.run()


    def stop(self):
        self.running = False



if __name__ == '__main__':
    filler = Filler()
    filler.start()
