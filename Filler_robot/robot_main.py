from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.PumpStation.pumps import Pump_station
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
        self.pump_station = Pump_station()
        self.robot = Robot_module(self.camera, self.neuron, self.interface, self.pump_station)

        self.camera_on = camera_on
        self.neuron_on = neuron_on 
        self.interface_on = interface_on
        self.robot_on = robot_on

        self.filler = False
        self.calibration_func = False
        self.view = False
        self.cip = False

        self.button_error = False 
        
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

        i = 0

        print('self.running', self.running)

        while self.running:
            self.i += 1
            print(self.i)
            # temp = check_temperature()
            # write_to_file(temp, 'log_temp.txt')

            if self.view:
                if self.camera_on: self.camera.running()
                if self.neuron_on: self.neuron.find_objects()
                if self.interface_on: self.interface.running()
 
            if self.filler:
                if self.camera_on: self.camera.running()
                if self.neuron_on: self.neuron.find_objects()
                if self.interface_on: self.interface.running()
                if self.robot_on: self.robot.running()
 
            if self.calibration_func:
                self.robot.calibration()
                
                if not self.button_error: self.prepare.emit()

                self.pumping()

                self.calibratiom_func = False

                # self.stop()

            if self.cip:
                self.pump_station.run()

                self.cip_stop()

            
            QThread.msleep(100)

        self.camera.stop()


    def view_run(self):
        self.view = True
        self.filler = False
        self.calibratiom_func = False
        self.cip = False

    def view_stop(self):
        self.view = False


    def filler_run(self):
        self.view = False
        self.filler = True
        self.calibration_func = False
        self.cip = False


    def filler_stop(self):
        self.filler = False


    def calibration_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = True
        self.cip = False


    def calibration_stop(self):
        self.calibration_func = False

    
    def cip_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = True


    def cip_stop(self):
        self.cip = False


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

        while not self.robot.find and self.calibration_func:
            if self.camera_on: self.camera.running()
            if self.neuron_on: self.neuron.find_objects()
            if self.robot_on: self.robot.running()

            if self.robot.find:
                self.robot.find = False
                break

            QThread.msleep(100)
            
            print(' Не нашел')
        
        print('нашел')

        if self.calibration_func:
            if not self.button_error: self.prepare.emit()

            self.robot.pump_station.run()
            if not self.button_error: self.prepare.emit()
            self.robot.go_home()
        
            if not self.button_error: self.prepare.emit()

            self.robot.pumping_find = False
            self.robot.find = False


    def stop_pumping(self):
        self.robot.pump_station.stop_pumps2()

    # def start_filler(self):
    #     self.filler_run = True

    def on_button_error(self):
        self.button_error = True


    def no_button_error(self):
        self.robot.no_stop_motors()

        self.button_error = False

        self.calibration_stop()