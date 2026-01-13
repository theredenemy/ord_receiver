import pydirectinput
import time

def move_pawn(input, hold=1):
    pydirectinput.keyDown(input)
    time.sleep(hold)
    pydirectinput.keyUp(input)
    return True