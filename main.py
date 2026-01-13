import ord_reader
from ord_reader import OrdInput
import ord_pawn
import pydirectinput
import obsws_python as obs
import time

ord = OrdInput()
move_cam = False
pid = ord_reader.get_pid("notepad.exe")

@ord.start
def start_ord():
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

if __name__ == '__main__':
    ord_reader.read_inputs("inputs.txt")
