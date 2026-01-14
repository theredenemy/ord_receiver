import ord_reader
from ord_reader import OrdInput
import ord_pawn
import pydirectinput
import vid2vtf
import processchecklib
import obsws_python as obs
import time
import shutil
import configHelper
from makeConfig import makeConfig
import fileinuse_functions
import os
import pathlib
import paramiko

ord = OrdInput()
move_cam = False
process_name = "notepad.exe"
cl = obs.ReqClient(host="localhost", port=4455)
maindir = os.getcwd()
config_file = "receiver.ini"
if not os.path.isfile(config_file):
    makeConfig()
inputs_file = "inputs.txt"
host = configHelper.read_config(config_file, "sftp", "host", default_value="127.0.0.1")
port = configHelper.read_config(config_file, "sftp", "port", default_value=21, is_int=True)
user = configHelper.read_config(config_file, "sftp", "user", default_value="fsky")
ssh_keyfile = configHelper.read_config(config_file, "sftp", "key", default_value="C:\\Users\\FSKY\\.ssh\\kulcs"),

@ord.start
def start_ord():
    status = cl.get_record_status()
    rec_active = status.output_active
    if rec_active:
        resp = cl.stop_record()
        recording = resp.output_path
        while(fileinuse_functions.is_file_in_use(recording) == True):
            pass
    cl.set_current_program_scene("ord_ren")
    cl.start_record()
    if not processchecklib.process_check(process_name):
        #ord_reader.endinput = True
        time.sleep(5)
        return
    pid = ord_reader.get_pid(process_name)
    print("start")

@ord.input("RENDER")
def ren():
    time.sleep(3)

@ord.input("XU")
def xufunc():
    print("XU")

@ord.input("ZU")
def zufunc():
   print("ZU")

@ord.input("ZD")
def zdfunc():
   print("ZD")

@ord.input("XD")
def xdfunc():
    print("XD")

@ord.input("YD")
def ydfunc():
    print("YD")

@ord.input("YU")
def yufunc():
    print("YU")

@ord.input("A")
def afunc():
    print("A")

@ord.input("B")
def bfunc():
    print("B")

@ord.input("C")
def cfunc():
    print("C")

@ord.eom
def eom():
    print("EOM")
    resp = cl.stop_record()
    recording = resp.output_path
    print(recording)
    while(fileinuse_functions.is_file_in_use(recording) == True):
        pass
    if not os.path.isdir("views"):
        os.mkdir("views")
    number = 1
    while True:
        if os.path.isdir(f"views\\view_{number}") == False:
            dir = f"views\\view_{number}"
            break
        else:
            number = number + 1
    os.mkdir(dir)
    filename = pathlib.Path(recording).stem
    fileext = pathlib.Path(recording).suffix
    view_dir = os.path.join(maindir, dir)
    shutil.move(recording, f"{view_dir}\\view{fileext}")
    print(f"Moved {recording} to {view_dir}\\view{fileext}")
    shutil.move(f"{maindir}\\{inputs_file}", f"{view_dir}\\{inputs_file}")
    print(f"Moved {inputs_file} to {view_dir}\\{inputs_file}")
    vid2vtf.video_to_vtf(video=f"{view_dir}\\view{fileext}", fps=15, width=256, height=128, output_dir=view_dir)
    materials_dir = os.path.join(view_dir, "materials")
    sound_dir = os.path.join(view_dir, "sound")
    ssh_client = paramiko.SSHClient()

    ssh_client.load_system_host_keys()

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting")
    ssh_client.connect(hostname=host, port=port, username=user, allow_agent=True, key_filename=ssh_keyfile)
    print("Connected")
    sftp = ssh_client.open_sftp()
    print("Uploading Files")
    for file in os.listdir(materials_dir):
        filepath = os.path.join(materials_dir, file)
        basefile = os.path.basename(filepath)
        if os.path.isfile(filepath):
            print(filepath)
            sftp.put(localpath=filepath, remotepath=f"/tf/materials/{basefile}" )
    
    for file in os.listdir(sound_dir):
        filepath = os.path.join(sound_dir, file)
        basefile = os.path.basename(filepath)
        if os.path.isfile(filepath):
            print(filepath)
            sftp.put(localpath=filepath, remotepath=f"/tf/sound/{basefile}" )
    
    sftp.close()
    ssh_client.close()
    cl.disconnect()

    
    


if __name__ == '__main__':
    if os.path.isfile(inputs_file):
        ord_reader.read_inputs(inputs_file)
