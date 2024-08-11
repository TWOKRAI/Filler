from PyQt5.QtCore import QThread, pyqtSignal

from Filler_robot.robot_main import Robot_filler
from Filler_robot.PumpStation.pumps import Pump_station

from Raspberry.input import Input_request


from Filler_interface.app import app
from Filler_interface.filler import filler


class Thread():
    def __init__(self):
        self.input_request = Input_request()
        self.robot_filler = Robot_filler()


    def start_input_thread(self):
        if not self.input_request.isRunning():
            if app.ready == True:
                self.input_request.show_error.connect(app.window_error.show)
                self.input_request.error.connect(self.stop_robot_thread)
                # self.input_request.error.connect(self.stop_pumps_thread)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)
                
                self.input_request.close_error.connect(app.window_error.close)

                self.input_request.motor_monitor.on_signal.connect(app.window_start.close)
                self.input_request.motor_monitor.button_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
                # self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)

                self.input_request.error.connect(app.window_view.close)

            self.input_request.start()


    def stop_input_thread(self):
        self.input_request.stop()


    def start_robot_thread(self):
        if not self.robot_filler.isRunning():
            if app.ready == True:
                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                app.window_prepare.calibration.connect(self.robot_filler.calibration)
                app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                app.window_prepare.find_cup.connect(self.robot_filler.find_cup)
                app.window_prepare.pumping.connect(self.robot_filler.pumping)
                # app.window_prepare.stop_pumping.connect(self.robot_filler.robot.pump_station.stop_pumps2)
                # app.window_prepare.start_filler.connect(self.robot_filler.run2)
                
                self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.robot_filler.start()


    def stop_robot_thread(self):
        self.robot_filler.stop()



