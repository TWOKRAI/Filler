from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.Robots.robot_module import Robot_module

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot_filler(QThread):
    prepare = pyqtSignal()

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

        self.calibratiom_func = False
        self.filler_run = False
        
        clear_file('log_temp.txt')

        self.i = 0


    def stop(self):
        self.running = False
        print('stop thread')
    

    def run(self) -> None:
        print('START THREAD')

        self.running = True
        self.robot.pumping_find = False
        self.robot.find = False
        
        self.filler_run = False

        i = 0

        print('self.running', self.running)

        while self.running:
            self.i += 1
            print(self.i)
            # temp = check_temperature()
            # write_to_file(temp, 'log_temp.txt')
        
            if self.filler_run:
                if self.camera_on: self.camera.running()
                if self.neuron_on: self.neuron.find_objects()
                if self.interface_on: self.interface.running()
                if self.robot_on: self.robot.running()
 
            if self.calibratiom_func:
                print('calibration 0')
                self.robot.calibration()
                print('calibration')
                self.prepare.emit()

                self.pumping()

                self.calibratiom_func = False
                self.robot.calibration_ready = True

                # self.stop()
            
            QThread.msleep(100)

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


    def reset_calibration(self):
        self.robot.calibration_ready = False

        self.robot.pumping_find = False
        self.robot.find = False

        self.robot.enable_motors(False)

        print('reset')


    def pumping(self):
        self.robot.pumping_find = True
        self.robot.find = False
        
        self.robot_on = True

        while not self.robot.find:
            if self.camera_on: self.camera.running()
            if self.neuron_on: self.neuron.find_objects()
            if self.robot_on: self.robot.running()

            if self.robot.find:
                self.robot.find = False
                break
            
            print(' Не нашел')
        
        print('нашел')

        self.prepare.emit()

        self.robot.pump_station.run()
        self.prepare.emit()
        self.robot.go_home()
    
        self.prepare.emit()

        self.robot.pumping_find = False
        self.robot.find = False

    
    # def pumping(self):
    #     self.robot.pump_station.run()
    #     self.robot.go_home()
    #     self.robot.calibration_ready = True

    #     self.prepare.emit()


    def stop_pumping(self):
        self.robot.pump_station.stop_pumps2()


    def start_filler(self):
        self.filler_run = True
        
        # print('START', self.robot_on)
        # self.run()

