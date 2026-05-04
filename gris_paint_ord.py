import traceback
import ord_reader
from ord_reader import OrdInput
import ord_pawn
import pydirectinput
import vid2vtf
import processchecklib
import obsws_python as obs
import time
import subprocess
import shutil
import configHelper
from makeConfig import makeConfig
import fileinuse_functions
import win32_functions
import os
import pathlib
import UploadFiles
import win32gui
import win32api
from count_steps import count_steps
if not processchecklib.process_check("obs64.exe"):
        processloop = 0
        os.system('del %Appdata%\\obs-studio\\.sentinel\\ /f /q')
        subprocess.Popen("C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe", cwd="C:\\Program Files\\obs-studio\\bin\\64bit")
        while (processloop < 1):
            if win32_functions.get_pid("obs64.exe"):
                processloop = 1
                break
time.sleep(3)
ord = OrdInput()
upload = True
hold_time = 0.1

while True:
    try:
        cl = obs.ReqClient(host="localhost", port=4455)
        break
    except Exception as e:
        print(type(e).__name__)
        error = traceback.format_exc()
        print(error)
scene_name = "ordinance"
scene_item_name = "INVAILD_INPUT"
maindir = os.getcwd()
config_file = "receiver.ini"
process_name = configHelper.read_config(config_file, "gris", "process_name", default_value="gris_paint.exe")
program_dir = configHelper.read_config(config_file, "gris", "program_dir", default_value="C:\\Users\\ORD_USER\\Documents\\gris_paint")
if not os.path.isfile(config_file):
    makeConfig()
inputs_file = "inputs.txt"
host = configHelper.read_config(config_file, "sftp", "host", default_value="127.0.0.1")
port = configHelper.read_config(config_file, "sftp", "port", default_value=21, is_int=True)
user = configHelper.read_config(config_file, "sftp", "user", default_value="fsky")
ssh_keyfile = configHelper.read_config(config_file, "sftp", "key", default_value="C:\\Users\\FSKY\\.ssh\\kulcs")
ord_server_ip = configHelper.read_config(config_file, "ORD_SERVER", "ip", default_value="10.0.0.246")
ord_server_port = configHelper.read_config(config_file, "ORD_SERVER", "port", default_value=5000, is_int=True)
ord_key = configHelper.read_config(config_file, "ORD_SERVER", "key", default_value="PUT_KEY_HERE")

def invaild_input(state=True):
    resp = cl.get_scene_item_list(scene_name)
    scene_items = [item['sourceName'] for item in resp.scene_items]
    if not scene_item_name in scene_items:
        settings = {
            "file": f"{maindir}\\imgs\\noinput.png",
            "unload": True
        }
        cl.create_input(sceneName=scene_name, inputName=scene_item_name, inputKind="image_source", inputSettings=settings, sceneItemEnabled=False)
    resp = cl.get_scene_item_id(scene_name, scene_item_name)
    item_id = resp.scene_item_id

    cl.set_scene_item_enabled(scene_name, item_id, state)
# START
@ord.start
def start_ord():
    if os.path.isfile(os.path.join(program_dir, "redraw.lock")):
        while(fileinuse_functions.is_file_in_use(os.path.join(program_dir, "redraw.lock")) == True):
            pass
        if os.path.isfile(os.path.join(program_dir, "redraw.lock")):
            os.remove(os.path.join(program_dir, "redraw.lock"))
    status = cl.get_record_status()
    scene_list = cl.get_scene_list()
    scenes = [scene['sceneName'] for scene in scene_list.scenes]
    rec_active = status.output_active
    if rec_active:
        resp = cl.stop_record()
        recording = resp.output_path
        while(fileinuse_functions.is_file_in_use(recording) == True):
            pass
    if not scene_name in scenes:
        cl.create_scene(scene_name)
    cl.set_current_program_scene(scene_name)
    
    if not win32_functions.get_pid_window(process_name):
        ord_reader.endinput = True
        subprocess.Popen(os.path.join(program_dir, process_name), cwd=program_dir)
        while not win32_functions.get_pid_window(process_name):
            pass
        
        time.sleep(5)
        cl.start_record()
        time.sleep(0.2)
        pydirectinput.press("m")
        return
    cl.start_record()
    time.sleep(0.2)
    pydirectinput.press("m")
    win32_functions.set_focus_win32(process_name)
    pid = ord_reader.get_pid(process_name)
    window = win32_functions.GetHwndsFromPID(win32_functions.get_pid_window(process_name))[0]

    x, y = win32_functions.get_window_x_y(window)
    win32api.SetCursorPos((x, y))
    print("start")
    pydirectinput.press("m")
@ord.invaild
def ord_invalid():
    invaild_input(True)
    time.sleep(3)
    invaild_input(False)
@ord.before_input
def before():
    if process_name == win32_functions.GetForegroundWindowProcessName():
        return True
    if not win32_functions.get_pid_window(process_name):
        ord_reader.endinput = True
        return False
    else:
        win32_functions.set_focus_win32(process_name)
        window = win32_functions.GetHwndsFromPID(win32_functions.get_pid_window(process_name))[0]

        x, y = win32_functions.get_window_x_y(window)

        rect = win32gui.GetWindowRect(window)
        if rect:
            win32api.ClipCursor(rect)
        return True


@ord.input("RENDER")
def ren():
    time.sleep(5)
    ord_reader.endinput = True

@ord.input("XU", True)
def xufunc(num):
    if num > 1:
        print(f"XUx{num}")
        hold = count_steps(hold_time, num)
    else:
        print("XU")
        hold = hold_time
    ord_pawn.move_pawn('right', hold)
    

@ord.input("ZU", True)
def zufunc(num):
    if num > 1:
        print(f"ZUx{num}")
        hold = count_steps(hold_time, num)
    else:
        print("ZU")
        hold = hold_time
    ord_pawn.move_pawn('up', hold)

@ord.input("ZD", True)
def zdfunc(num):
    if num > 1:
        print(f"ZDx{num}")
        hold = count_steps(hold_time, num)
    else:
        print("ZD")
        hold = hold_time
    ord_pawn.move_pawn('down', hold)

@ord.input("XD", True)
def xdfunc(num):
    if num > 1:
        print(f"XDx{num}")
        hold = count_steps(hold_time, num)
    else:
        print("XD")
        hold = hold_time
    ord_pawn.move_pawn('left', hold)
# @ord.input("YD")
# def ydfunc():
#     print("YD")
#     pydirectinput.press('down')

# @ord.input("YU")
# def yufunc():
#     print("YU")
#     pydirectinput.press('up')

@ord.input("A")
def afunc():
    print("A")
    pydirectinput.press('a')

@ord.input("B")
def bfunc():
    print("B")
    pydirectinput.press('b')

@ord.input("C")
def cfunc():
    print("C")
    pydirectinput.press('c')

@ord.input("CB")
def CBFunc():
    print("AB")
    if not ord_reader.input_chain_on:
        ord_reader.input_chain_on = True
        print("Input Chain is now on")
    else:
        ord_reader.input_chain_on = False
        print("Input Chain is now off")

@ord.eom
def eom():
    if os.path.isfile(os.path.join(program_dir, "redraw.lock")):
        while(fileinuse_functions.is_file_in_use(os.path.join(program_dir, "redraw.lock")) == True):
            pass
        if os.path.isfile(os.path.join(program_dir, "redraw.lock")):
            os.remove(os.path.join(program_dir, "redraw.lock"))

    print("EOM")
    win32api.ClipCursor((0,0,0,0))
    time.sleep(6)
    if not processchecklib.process_check(process_name):
        invaild_input(True)
        time.sleep(5)
        invaild_input(False)
        
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
    if upload:
        UploadFiles.upload_dir(materials_dir, "/tf/materials", host, port, user, ssh_keyfile)
        UploadFiles.upload_dir(sound_dir, "/tf/sound", host, port, user, ssh_keyfile)
        UploadFiles.upload_file(f"{view_dir}\\view{fileext}", "/tf/public", host, port, user, ssh_keyfile)
    
    cl.disconnect()

    
    


if __name__ == '__main__':
    if os.path.isfile(inputs_file):
        ord_reader.read_inputs(inputs_file, wait=0)
