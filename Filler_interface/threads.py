from PyQt5.QtCore import QThread

from Filler_robot.robot_main import Robot_filler
from Filler_robot.Monitor.motor_monitor import Motor_monitor

from Raspberry.input import Input_request


from Filler_interface.app import app


class Thread():
    def __init__(self):
        self.thread_robot = QThread()
        self.robot_filler = None

        self.thread_input = QThread()
        self.input = None


    def start_robot_thread(self, camera_on = True, neuron_on = True, interface_on = True, robot_on = False):
        if not self.thread_robot.isRunning():
            self.thread_robot = QThread()
            self.robot_filler = Robot_filler(camera_on = camera_on, neuron_on = neuron_on, interface_on = interface_on, robot_on = robot_on)
            self.robot_filler.moveToThread(self.thread_robot)

            if app.ready == True:
                self.thread_robot.started.connect(self.robot_filler.run)
                self.robot_filler.interface.frame_captured.connect(app.window_view.update_frame)
                self.input_request.error.connect(self.robot_filler.robot.stop_motors)
            
            self.thread_robot.start()
    

    def stop_robot_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.robot_filler.stop()
            self.thread_robot.quit()
            self.thread_robot.wait()
            # self.thread_robot = None
            # self.robot_filler = None


    def start_input_thread(self):
        if not self.thread_robot.isRunning():
            self.thread_input = QThread()
            self.input_request = Input_request()
            self.input_request.moveToThread(self.thread_input)
            self.thread_input.started.connect(self.input_request.run)

            if app.ready == True:
                self.input_request.show_error.connect(app.window_error.show)
                self.input_request.error.connect(self.stop_robot_thread)
                self.input_request.close_error.connect(app.window_error.close)

                self.input_request.motor_monitor.on_signal.connect(app.window_start.close)

                self.input_request.motor_monitor.off_signal.connect(app.window_start.show)
                self.input_request.motor_monitor.off_signal.connect(app.window_view.close)
                # self.input_request.motor_monitor.off_signal.connect(self.stop_input_thread)

                self.input_request.error.connect(app.window_view.close)

            self.thread_input.start()
    

    def stop_input_thread(self):
        if self.thread_robot is not None and self.thread_robot.isRunning():
            self.input_request.stop()
            self.thread_input.quit()
            self.thread_input.wait()
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


thread = Thread()