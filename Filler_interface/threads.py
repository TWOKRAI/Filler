from PyQt5.QtCore import QThread, pyqtSignal

from Filler_robot.robot_main import Robot_filler
from Filler_robot.PumpStation.pumps import Pump_station

from Raspberry.input import Input_request


from Filler_interface.app import app


class Thread():
    def __init__(self):
        self.thread_robot = QThread()
        self.robot_filler = None

        self.thread_input = QThread()
        self.input = None

        self.thread_pumps = QThread()
        self.pumps = None



    def robot_thread(self):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler()
            self.robot_filler.moveToThread(self.thread_robot)

    def startt_robot_view(self):
        self.robot_filler.camera_on = True
        self.robot_filler.neuron_on = True
        self.robot_filler.interface_on = True


        self.thread_robot.started.connect(self.robot_filler.run)




    def start_robot_thread(self, camera_on = False, neuron_on = False, interface_on = False, robot_on = False):
        # if not self.thread_robot.isRunning():
        #     self.thread_robot = QThread()
        #     self.robot_filler = Robot_filler(camera_on = camera_on, neuron_on = neuron_on, interface_on = interface_on, robot_on = robot_on)
        #     self.robot_filler.moveToThread(self.thread_robot)

            if app.ready == True:
                # self.robot_filler.robot.calibration_ready = True
                # self.robot_filler.robot.pumping_find = False

                #self.thread_robot.started.connect(self.robot_filler.run)


                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)

                app.window_prepare.calibration.connect(self.start_calibration)
                app.window_prepare.reset_calibration.connect(self.robot_filler.reset_calibration)
                app.window_prepare.find_cup.connect(self.find_cup)
                self.robot_filler.robot.prepare.connect(app.window_prepare.update_prepare)

            self.thread_robot.start()
    

    def stop_robot_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.robot_filler.stop()
            self.thread_robot.quit()
            self.thread_robot.wait()
            # self.thread_robot = None
            # self.robot_filler = None
    

    def start_calibration(self):
        if self.thread_robot.isRunning():
            self.thread_robot.quit()
            self.thread_robot.wait()
    
        self.thread_robot.started.connect(self.robot_filler.calibration)
        self.thread_robot.start()

    
    def find_cup(self):
        if self.thread_robot.isRunning():
            self.thread_robot.quit()
            self.thread_robot.wait()
    
        self.thread_robot.started.connect(self.robot_filler.find_cup)
        self.thread_robot.start()


    def start_input_thread(self):
        if not self.thread_input.isRunning():
            self.thread_input = QThread()
            self.input_request = Input_request()
            self.input_request.moveToThread(self.thread_input)
            self.thread_input.started.connect(self.input_request.run)

            if app.ready == True:
                self.input_request.show_error.connect(app.window_error.show)
                self.input_request.error.connect(self.stop_robot_thread)
                self.input_request.error.connect(self.stop_pumps_thread)
                
                self.input_request.close_error.connect(app.window_error.close)

                self.input_request.motor_monitor.on_signal.connect(app.window_start.close)
                self.input_request.motor_monitor.button_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
                # self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)

                self.input_request.error.connect(app.window_view.close)

            self.thread_input.start()
    

    def stop_input_thread(self):
        if self.thread_input is not None and self.thread_robot.isRunning():
            self.input_request.stop()
            self.thread_input.quit()
            self.thread_input.wait()
            # self.thread_robot = None
            # self.robot_filler = None


    def start_pumps_thread(self, pump1, pump2, speed_1, speed_2):
        if not self.thread_pumps.isRunning():
            self.thread_pumps = QThread()
            self.pumps = Pump_station()

            self.pumps.pump_1_enable = pump1
            self.pumps.pump_1.speed = speed_1

            self.pumps.pump_2_enable = pump2
            self.pumps.pump_2.speed = speed_2

            self.pumps.moveToThread(self.thread_pumps)
            self.thread_pumps.started.connect(self.pumps.run)

            if app.ready == True:
                app.window_cip.stop_pumps_signal.connect(self.stop)
                self.input_request.error.connect(self.stop)
                self.input_request.error.connect(self.stop_pumps_thread)

                self.pumps.minus_pump.connect(app.window_cip.close)
                
            self.thread_pumps.start()


    def stop(self):
        self.pumps.stop_pumps2()
    

    def stop_pumps_thread(self):
        self.thread_pumps.quit()
        self.thread_pumps.wait()

            # self.thread_robot = None
            # self.robot_filler = None


    # def start_monitor_thread(self):
    #     if not self.thread_robot.isRunning():
    #         self.thread_monitor = QThread()
    #         self.motor_monitor = Motor_monitor()
    #         self.motor_monitor.moveToThread(self.thread_monitor)
    #         self.thread_monitor.started.connect(self.motor_monitor.run)

    #         if app.ready == True:
    #             self.motor_monitor.show_error.connect(app.window_error.show)
    #             self.motor_monitor.error.connect(self.stop_robot_thread)
    #             self.motor_monitor.close_error.connect(app.window_error.close)

    #             self.motor_monitor.motor_monitor.on_signal.connect(app.window_start.close)

    #             self.motor_monitor.motor_monitor.off_signal.connect(app.window_start.show)
    #             self.motor_monitor.motor_monitor.off_signal.connect(app.window_view.close)
    #             self.motor_monitor.motor_monitor.off_signal.connect(self.stop_monitor_thread)

    #         self.thread_input.start()
    

    # def stop_monitor_thread(self):
    #     if self.thread_robot is not None and self.thread_robot.isRunning():
    #         self.motor_monitor.stop()
    #         self.thread_input.quit()
    #         self.thread_input.wait()
    #         # self.thread_robot = None
    #         # self.robot_filler = None


# thread = Thread()