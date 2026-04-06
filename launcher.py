import requests
import configHelper
import json
import os
config_file = "receiver.ini"

ord_server_ip = configHelper.read_config(config_file, "ORD_SERVER", "ip", default_value="10.0.0.100")
ord_server_port = configHelper.read_config(config_file, "ORD_SERVER", "port", default_value=5000, is_int=True)
url = f"http://{ord_server_ip}:{ord_server_port}/ord/mode"
data = requests.get(url)

json_data = json.loads(data.text)

mode = json_data.get('mode')

print(mode)

if mode == "game":
    os.system("python main.py")
elif mode == "draw":
    os.system("python gris_paint_ord.py")


