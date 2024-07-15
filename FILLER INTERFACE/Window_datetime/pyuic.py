import subprocess

subprocess.run(['pyuic5', 'Window_datetime/UI_datetime.ui', '-o', 'Window_datetime/datetime.py'], check=True)
