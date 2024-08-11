from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.Robots.robot_module import Robot_module

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot_filler(QThread):
    def __init__(self, camera_on = True, neuron_on = True, interface_on = True, robot_on = False) -> None:
        super().__init__()

        self.running = True

        self.camera = Camera()
        self.neuron = Neuron(self.camera)
        self.interface = Interface(self.camera, self.neuron)
        self.robot = Robot_module(self.camera, self.neuron, self.interface)

        self.camera_on = camera_on
        self.neuron_on = neuron_on 
        self.interface_on = interface_on
        self.robot_on = robot_on
        
        clear_file('log_temp.txt')

        self.i = 0


    def stop(self):
        self.running = False
    

    def run(self) -> None:
        self.running = True
        self.robot.pumping_find = False
        self.robot.find = False
        print('33333333333333333')

        while self.running:
            
            self.i += 1
            print(self.i)
            # temp = check_temperature()
            # write_to_file(temp, 'log_temp.txt')
            
            if self.camera_on: self.camera.running()
            if self.neuron_on: self.neuron.find_objects()
            if self.interface_on: self.interface.running()
            if self.robot_on: self.robot.running()

            # if self.robot_on: QThread.msleep(3000)

            # QThread.msleep(1000)

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


    def calibration(self):

        self.robot.calibration()
        print('calibration')


    def reset_calibration(self):
        self.robot.calibration_ready = False

        self.robot.pumping_find = False
        self.robot.find = False

        self.robot.enable_motors(False)

        print('reset')


    def find_cup(self):
        self.robot.pumping_find = True
        self.robot.find = False

        while self.running:
            if self.camera_on: self.camera.running()
            if self.neuron_on: self.neuron.find_objects()
            if self.robot_on: self.robot.running()

            if self.robot.find:
                self.robot.find = False
                break
        
        print('нашел')

        self.camera.stop()

    
    def pumping(self):
        self.robot.pump_station.run()
        self.robot.go_home()
        self.robot.ready_calibration()


    def stop_pumping(self):
        self.robot.pump_station.stop_pumps2()


    def start_filler(self):
        self.robot_on = True
        
        print('START', self.robot_on)
        self.run()

