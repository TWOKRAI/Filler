import subprocess


def get_cpu_temp():
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout.strip().split('=')[1]
    return float(temp_str.strip("'C"))


def get_cpu_temp_sys():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = int(f.read().strip()) / 1000
    return temp


def check_temperature(threshold=80):
    temp = get_cpu_temp()
    print(f"Temperature CPU: {temp} C")
    
    if temp > threshold:
        print(f"Error: Temperature CPU >= {threshold} C!")


check_temperature(threshold=70)