import UploadFiles
import vid2vtf
import os
import configHelper
import shutil
config_file = "receiver.ini"
host = configHelper.read_config(config_file, "sftp", "host", default_value="127.0.0.1")
port = configHelper.read_config(config_file, "sftp", "port", default_value=21, is_int=True)
user = configHelper.read_config(config_file, "sftp", "user", default_value="fsky")
ssh_keyfile = configHelper.read_config(config_file, "sftp", "key", default_value="C:\\Users\\FSKY\\.ssh\\kulcs")

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

