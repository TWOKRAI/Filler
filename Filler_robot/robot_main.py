from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import numpy as np

from Filler_robot.VisionTech.camera import Camera
from Filler_robot.NeuroModules.neuron import Neuron
from Filler_robot.NeuroModules.interface import Interface
from Filler_robot.PumpStation.pumps import Pump_station
from Filler_robot.Robots.robot_module import Robot_module
from Filler_robot.VisionTech.laser import Laser

from Raspberry.Temperature import check_temperature, write_to_file, clear_file


class Robot_filler(QThread):
    prepare = pyqtSignal()

    def __init__(self, camera_on = True, neuron_on = True, interface_on = True, robot_on = False) -> None:
        super().__init__()

        self.running = True

        self.camera = Camera()

        self.neuron = Neuron(self.camera)
    
        self.interface = Interface(self.camera, self.neuron)
        self.neuron.interface = self.interface

        self.pump_station = Pump_station()

        self.laser = Laser() 

        self.robot = Robot_module(self.camera, self.neuron, self.interface, self.pump_station, self.laser)
        
        self.camera_on = camera_on
        self.neuron_on = neuron_on 
        self.interface_on = interface_on
        self.robot_on = robot_on

        self.filler = False
        self.calibration_func = False
        self.view = False
        self.cip = False
        self.cip_move = False
        self.calibration_only = False

        self.first_view = False

        self.button_error = False 
        
        clear_file('log_temp.txt')

        self.i = 0
        self.time = 0

        self.robot.motor_z.enable_on(True)

        self.laser.on_off(0)


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
            if self.view:
                self.laser.on_off(1)

                if not self.first_view:
                    self.camera.running()
                    self.neuron.find_objects()
                    self.interface.running()
                    self.first_view = True

                self.camera.running()
                self.neuron.neuron_vision()

                self.interface.running()

                QThread.msleep(500)
 
            if self.filler:
                self.laser.on_off(1)

                self.camera.running()
                find_tuple = self.neuron.find_objects()

                if find_tuple[1] > 0:
                    if self.robot.calibration_ready == False:
                        self.robot.calibration()

                    self.laser.running()
                    self.laser.on_off(0)

                    self.camera.running()
                    self.neuron.neuron_vision()

                    self.time = 0

                self.interface.running()

                self.robot.running()

                #QThread.msleep(1500)
 
            if self.calibration_func:
                self.robot.calibration()
                
                if not self.button_error: self.prepare.emit()

                self.pumping()

                self.calibratiom_func = False

                # self.stop()

            if self.cip:
                self.pump_station.cip()
                self.cip_stop()

            if self.calibration_only:
                self.robot.calibration()

                self.laser.first_start()
                self.calibration_only = False

            if self.cip_move:
                self.robot.move_cip()

                self.cip_move_stop()

            
            if not self.filler and not self.view:
                self.laser.on_off(0)


            if self.time > 100:
                self.robot.enable_motors(False)
                self.pump_station.enable_motors(False)

                temp = check_temperature()
                write_to_file(temp, 'log_temp.txt')

                print('OFF TIMER')

                self.robot.calibration_ready = False 

                self.time = 0
                
                
            QThread.msleep(100)

            if self.filler:
                self.time += 1
            else:
                self.time += 0.1

        self.camera.stop()


    def starting(self):
        self.calibration_only_run()


    def view_run(self):
        self.view = True
        self.filler = False
        self.calibratiom_func = False
        self.cip = False
        self.cip_move = False

    def view_stop(self):
        self.view = False
        self.first_view = False


    def filler_run(self):
        self.view = False
        self.filler = True
        self.calibration_func = False
        self.cip = False
        self.cip_move = False

        self.time = 0


    def filler_stop(self):
        self.filler = False


    def calibration_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = True
        self.cip = False
        self.cip_move = False

        self.time = 0


    def calibration_stop(self):
        self.calibration_func = False

    
    def cip_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = True
        self.cip_move = False


    def cip_stop(self):
        self.cip = False


    def cip_move_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = False
        self.cip_move = True


    def cip_move_stop(self):
        self.cip_move = False


    def calibration_only_run(self):
        self.view = False
        self.filler = False
        self.calibration_func = False
        self.cip = False
        self.cip_move = False
        self.calibration_only = True


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

        self.laser.on_off(1)

        while not self.robot.find and self.calibration_func:
            self.camera.running()
            find_tuple = self.neuron.find_objects()
    
            if find_tuple[1] > 0:
                self.laser.running()
                self.laser.on_off(0)

                self.camera.running()
                self.neuron.neuron_vision()

            if self.robot_on: self.robot.running()

            if self.robot.find:
                self.robot.find = False
                break

            QThread.msleep(100)
            
            print(' Не нашел')
        
        print('нашел')

        if self.calibration_func:
            if not self.button_error: self.prepare.emit()

            self.pump_station.prepare()
            if not self.button_error: self.prepare.emit()
            self.robot.go_home()
        
            if not self.button_error: self.prepare.emit()

            self.robot.pumping_find = False
            self.robot.find = False


    def stop_pumping(self):
        self.robot.pump_station.stop_pumps2()


    def on_button_error(self):
        self.button_error = True


    def no_button_error(self):
        self.robot.no_stop_motors()

        self.button_error = False
        

        self.calibration_stop()
