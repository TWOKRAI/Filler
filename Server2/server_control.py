import subprocess
import time


class Server_module:
    def __init__(self) -> None:
        pass

    def run(self):
        self.stop()
        time.sleep(1)
        subprocess.Popen(['/bin/bash', '-c', 'source /home/innotech/Project/Filler/Server/myenv/bin/activate && python /home/innotech/Project/Filler/Server/myproject/manage.py runserver 0.0.0.0:8000'])
        
    def stop(self):
        subprocess.Popen(['pkill', '-f', 'python /home/innotech/Project/Filler/Server/myproject/manage.py runserver 0.0.0.0:8000'])


server = Server_module()