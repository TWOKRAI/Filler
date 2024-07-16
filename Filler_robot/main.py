from camera import camera 
from neuron import neuron
from interface import interface
from robot import robot


class Filler:
    def __init__(self) -> None:
        self.camera_on = True
        self.robot_on = False
        self.inteface_on = True
        self.neuron_on = True

    
    def run(self) -> None:
        if self.robot_on: robot.go_home()

        while True:
            if self.camera_on: camera.run()
            if self.neuron_on: neuron.run() 
            if self.inteface_on: interface.run()
            if self.robot_on: robot.run()


if __name__ == '__main__':
    filler = Filler()
    filler.run()
