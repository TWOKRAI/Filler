# import multiprocessing
# import subprocess
# import time


# class ServerManager:
#     def __init__(self):
#         self.server_process = None
#         self.server_module_process = None

#     def run_server(self):
#         self.server_module_process = subprocess.Popen(
#             ['/bin/bash', '-c', 'source /home/innotech/Project/Filler/Server2/myenv/bin/activate && python /home/innotech/Project/Filler/Server2/myproject/manage.py runserver 0.0.0.0:8000'],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL
#         )


#     def stop_server(self):
#         subprocess.Popen(['pkill', '-f', 'python /home/innotech/Project/Filler/Server2/myproject/manage.py runserver 0.0.0.0:8000'])


#     def start_server(self):
#         self.stop_server_process()
#         time.sleep(1)
#         if self.server_process is None or not self.server_process.is_alive():
#             self.server_process = multiprocessing.Process(target=self.run_server)
#             self.server_process.start()


#     def stop_server_process(self):
#         self.stop_server()

#         if self.server_process is not None and self.server_process.is_alive():
#             self.stop_server()
#             self.server_process.terminate()
#             self.server_process.join()
#             self.server_process = None



# if __name__ == "__main__":
#     server = ServerManager()
#     server.start_server()


import multiprocessing
import subprocess
import time

class ServerManager:
    def __init__(self):
        self.server_process = None

    def run_server(self):
        try:
            subprocess.run(
                ['/bin/bash', '-c', 'source /home/innotech/Project/Filler/Server2/myenv/bin/activate && python /home/innotech/Project/Filler/Server2/myproject/manage.py runserver 0.0.0.0:8000'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running server: {e}")

    def stop_server(self):
        try:
            subprocess.run(
                ['pkill', '-f', 'python /home/innotech/Project/Filler/Server2/myproject/manage.py runserver 0.0.0.0:8000'],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error stopping server: {e}")

    def start_server(self):
        self.stop_server_process()
        time.sleep(1)
        if self.server_process is None or not self.server_process.is_alive():
            self.server_process = multiprocessing.Process(target=self.run_server)
            self.server_process.start()

    def stop_server_process(self):
        self.stop_server()

        if self.server_process is not None and self.server_process.is_alive():
            self.server_process.terminate()
            self.server_process.join()
            self.server_process = None


if __name__ == "__main__":
    server = ServerManager()
    server.start_server()