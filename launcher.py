import requests
import configHelper
import json
import os
import win32_functions
config_file = "receiver.ini"

ord_server_ip = configHelper.read_config(config_file, "ORD_SERVER", "ip", default_value="10.0.0.100")
ord_server_port = configHelper.read_config(config_file, "ORD_SERVER", "port", default_value=5000, is_int=True)
url = f"http://{ord_server_ip}:{ord_server_port}/ord/info"
data = requests.get(url)

json_data = json.loads(data.text)

mode = json_data.get('mode')

print(mode)

if mode == "game":
    if win32_functions.get_pid_window("gris_paint.exe"):
        os.system("taskkill /f /im gris_paint.exe")
    os.system("python main.py")
elif mode == "draw":
    if win32_functions.get_pid_window("DELTARUNE.exe"):
        os.system("taskkill /f /im DELTARUNE.exe")
    os.system("python gris_paint_ord.py")


