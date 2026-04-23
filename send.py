import UploadFiles
import vid2vtf
import os
import configHelper
import shutil
import requests
import json
config_file = "receiver.ini"
host = configHelper.read_config(config_file, "sftp", "host", default_value="127.0.0.1")
port = configHelper.read_config(config_file, "sftp", "port", default_value=21, is_int=True)
user = configHelper.read_config(config_file, "sftp", "user", default_value="fsky")
ord_server_ip = configHelper.read_config(config_file, "ORD_SERVER", "ip", default_value="10.0.0.100")
ord_server_port = configHelper.read_config(config_file, "ORD_SERVER", "port", default_value=5000, is_int=True)
ssh_keyfile = configHelper.read_config(config_file, "sftp", "key", default_value="C:\\Users\\FSKY\\.ssh\\kulcs")
ord_key = configHelper.read_config(config_file, "ORD_SERVER", "key", default_value="PUT_KEY_HERE")
url = f"http://{ord_server_ip}:{ord_server_port}/ord/info"
data = requests.get(url, headers={'X-ORD-KEY': ord_key})

json_data = json.loads(data.text)

state = json_data.get('state')

if not state == 'dead':
    view_vid = "view.mp4"
    view_dir = os.path.join(os.getcwd(), "startup_view")
    if not os.path.isdir(view_dir):
        os.mkdir(view_dir)
    if os.path.isfile(f"{view_dir}\\{view_vid}"):
        os.remove(f"{view_dir}\\{view_vid}")
    shutil.copy(view_vid, f"{view_dir}\\{view_vid}")
    vid2vtf.video_to_vtf(video=f"{view_dir}\\{view_vid}", fps=15, width=256, height=128, output_dir=view_dir)
    materials_dir = os.path.join(view_dir, "materials")
    sound_dir = os.path.join(view_dir, "sound")
    UploadFiles.upload_dir(materials_dir, "/tf/materials", host, port, user, ssh_keyfile)
    UploadFiles.upload_dir(sound_dir, "/tf/sound", host, port, user, ssh_keyfile)
    UploadFiles.upload_file(f"{view_dir}\\{view_vid}", "/tf/public", host, port, user, ssh_keyfile)



