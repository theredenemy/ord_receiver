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
import requests
import psutil
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
move_cam = False
upload = True
hold_time = 0.1
sprint = False
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
game_dir = configHelper.read_config(config_file, "delta", "game_dir", default_value="C:\\Users\\ORD_USER\\Documents\\DELTARUNE_ORD")
process_name = configHelper.read_config(config_file, "delta", "process_name", default_value="DELTARUNE_ORD.exe") 

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
def check_if_game_end():
    while fileinuse_functions.is_file_in_use(os.path.join(game_dir, "end.txt")):
        pass
    with open(os.path.join(game_dir, "end.txt"), 'r', encoding="utf-8", errors='ignore') as f:
        end_str = str(f.read())
        end = int(end_str.strip())

        if end == 1:
            return True
        else:
            return False
def check_if_hold_game():
    with open(os.path.join(game_dir, "hold.txt"), 'r', encoding="utf-8", errors='ignore') as f:
        
        hold_str = str(f.read())
        # why the fuck did this just break
        # this will fix it i hope it does
        # FUCK
        # it was the mod
        hold = int(hold_str.strip())
        if hold == 1:
            return True
        else:
            return False
# START
@ord.start
def start_ord():
    while True:
        try:
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
            break
        except obs.error.OBSSDKRequestError:
            pass
    cl.start_record()

    if not processchecklib.process_check(process_name):
        ord_reader.endinput = False
        subprocess.Popen(os.path.join(game_dir, process_name), cwd=game_dir)
        while not win32_functions.get_pid_window(process_name):
            pass
        if not win32_functions.GetForegroundWindowProcessName() == process_name:
            win32_functions.set_focus_win32(process_name)
        
        time.sleep(5)
        # i changed the deltarune mod code so no need for this
        # time.sleep(150)
        time.sleep(20)
        if check_if_hold_game():
            while check_if_hold_game():
                pass
        pydirectinput.press("z")
        time.sleep(2)
        pydirectinput.press("z")
        time.sleep(5)
        # if this fails check gml_Object_DEVICE_CONTACT_Step_0 In Mod Or gml_Object_DEVICE_CONTACT_Create_0 In Mod Or Check This Code
        if check_if_hold_game():
            while check_if_hold_game():
                pass
        # time.sleep(60)
        time.sleep(10)
        return
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            proc.resume()

    win32_functions.set_focus_win32(process_name)
    pid = win32_functions.get_pid(process_name)
    window = win32_functions.GetHwndsFromPID(win32_functions.get_pid(process_name))[0]

    x, y = win32_functions.get_window_x_y(window)
    win32api.SetCursorPos((x, y))
    print("start")
@ord.invaild
def ord_invalid():
    invaild_input(True)
    time.sleep(3)
    invaild_input(False)
@ord.before_input
def before():
    if check_if_hold_game():
        while check_if_hold_game():
            pass
    if check_if_game_end():
        ord_reader.endinput = True
        return False
    
    
        

    
    if process_name == win32_functions.GetForegroundWindowProcessName():
        return True
    if not win32_functions.get_pid_window(process_name):
        ord_reader.endinput = True
        return False
    else:
        win32_functions.set_focus_win32(process_name)
        window = win32_functions.GetHwndsFromPID(win32_functions.get_pid(process_name))[0]

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
    if ord_reader.input_chain_on:
        if num > 1:
            print(f"XUx{num}")
            hold = count_steps(hold_time, num)
        else:
            print("XU")
            hold = hold_time
        ord_pawn.move_pawn('right', hold)
    else:
        pydirectinput.keyDown("right")
        pydirectinput.keyUp("right")
    

@ord.input("ZU", True)
def zufunc(num):
    if ord_reader.input_chain_on:
        if num > 1:
            print(f"ZUx{num}")
            hold = count_steps(hold_time, num)
        else:
            print("ZU")
            hold = hold_time
        ord_pawn.move_pawn('up', hold)
    else:
        pydirectinput.keyDown("up")
        pydirectinput.keyUp("up")

@ord.input("ZD", True)
def zdfunc(num):
    if ord_reader.input_chain_on:
        if num > 1:
            print(f"ZDx{num}")
            hold = count_steps(hold_time, num)
        else:
            print("ZD")
            hold = hold_time
        ord_pawn.move_pawn('down', hold)
    else:
        pydirectinput.keyDown("down")
        pydirectinput.keyUp("down")

@ord.input("XD", True)
def xdfunc(num):
    if ord_reader.input_chain_on:
        if num > 1:
            print(f"XDx{num}")
            hold = count_steps(hold_time, num)
        else:
            print("XD")
            hold = hold_time
        ord_pawn.move_pawn('left', hold)
    else:
        pydirectinput.keyDown("left")
        pydirectinput.keyUp("left")

@ord.input("YD")
def ydfunc():
    print("YD")
    pydirectinput.press('down')

@ord.input("YU")
def yufunc():
    print("YU")
    pydirectinput.press('up')

@ord.input("A")
def afunc():
    print("A")
    pydirectinput.press('z')

@ord.input("B")
def bfunc():
    print("B")
    pydirectinput.press('x')

@ord.input("C")
def cfunc():
    print("C")
    pydirectinput.press('c')

@ord.input("AA")
def wait5():
    print("AA")
    time.sleep(5)

@ord.input("AC")
def acfunc():
    print("AC")
    pydirectinput.press('z')

@ord.input("BC")
def bcfunc():
    print("BC")
    pydirectinput.press('x')

@ord.input("CC")
def ccfunc():
    print("CC")
    pydirectinput.press('c')

@ord.input("AB")
def abfunc():
    global sprint
    print("AB")
    # fix
    if not sprint:
        pydirectinput.keyDown("x")
        sprint = True
        print("Sprint is now on")
    else:
        pydirectinput.keyUp("x")
        sprint = False
        print("Sprint is now off")

@ord.input("CA")
def cafunc():
    print("CA")
    time.sleep(1)
@ord.input("CB")
def CBFunc():
    print("CB")
    if not ord_reader.input_chain_on:
        ord_reader.input_chain_on = True
        print("Input Chain is now on")
    else:
        ord_reader.input_chain_on = False
        print("Input Chain is now off")
@ord.input("BB")
def BBFunc():
    print("BB")
    time.sleep(0.1)
@ord.eom
def eom():
    global sprint
    ending = check_if_game_end()
    if check_if_hold_game():
        while check_if_hold_game():
            pass
    if sprint:
        pydirectinput.keyUp("x")
        sprint = False
        print("Sprint is now off")

    print("EOM")
    win32api.ClipCursor((0,0,0,0))
    if check_if_hold_game():
        while check_if_hold_game():
            pass
    if processchecklib.process_check(process_name) and not ending:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.suspend()
    #time.sleep(6)
    if not processchecklib.process_check(process_name) and not ending:
        invaild_input(True)
        time.sleep(5)
        invaild_input(False)
        json_data = {'state': 'dead'}
        url = f"http://{ord_server_ip}:{ord_server_port}/ord/pawn/state"
        requests.post(url, json=json_data, headers={'X-ORD-KEY': ord_key})
    if check_if_game_end():
        while check_if_game_end():
            pass
        for i in range(5):
            invaild_input(True)
            time.sleep(1)
            invaild_input(False)
            time.sleep(1)
        if os.path.isfile("end_game.cmd"):
            os.system("end_game.cmd")
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
    shutil.move(recording, f"{view_dir}\\view_og{fileext}")
    print(f"Moved {recording} to {view_dir}\\view_og{fileext}")
    video_name = "view.mp4"
    os.system(f'ffmpeg -y -i {os.path.join(view_dir, f"view_og{fileext}")} -vf "scale=256:128" -ar 11025 {os.path.join(view_dir, video_name)}')
    shutil.move(f"{maindir}\\{inputs_file}", f"{view_dir}\\{inputs_file}")
    print(f"Moved {inputs_file} to {view_dir}\\{inputs_file}")
    vid2vtf.video_to_vtf(video=os.path.join(view_dir, video_name), fps=15, width=256, height=128, output_dir=view_dir)
    materials_dir = os.path.join(view_dir, "materials")
    sound_dir = os.path.join(view_dir, "sound")
    if upload:
        UploadFiles.upload_dir(materials_dir, "/tf/materials", host, port, user, ssh_keyfile)
        UploadFiles.upload_dir(sound_dir, "/tf/sound", host, port, user, ssh_keyfile)
        UploadFiles.upload_file(os.path.join(view_dir, video_name), "/tf/public", host, port, user, ssh_keyfile)
    
    cl.disconnect()

    
    


if __name__ == '__main__':
    if os.path.isfile(inputs_file):
        ord_reader.read_inputs(inputs_file, ord, wait=0.1)
