import os
import pydirectinput
import time
import psutil

maindir = os.getcwd()
endinput = False
class OrdInput:
    def __init__(self):
        self.registry = {}
        self.eom_func = None
        self.start_func = None
        self.invalid_func = None
        self.before_input_func = None
    def start(self, func):
        self.start_func = func
        return func
    def input(self, input):
        def wrapper(func):
            self.registry[input] = func
            return func
        return wrapper
    def eom(self, func):
        self.eom_func = func
        return func
    def invaild(self, func):
        self.invalid_func = func
        return func
    def before_input(self, func):
        self.before_input_func = func
        return func
    def start_ord(self):
        if self.start_func:
            self.start_func()
    
    def make_input(self, input):
        if self.before_input_func:
            state = self.before_input_func()
            if state is False:
                return
        if input in self.registry:
            self.registry[input]()
        else:
            print(f"INVAILD INPUT : {input}")
            if self.invalid_func:
                self.invalid_func()
    def run_eom(self):
        if self.eom_func:
            self.eom_func()


def get_pid(process_name):
    pid = None
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            pid = proc.info['pid']
            return pid

def getmaxlines(filename):
    linenum = 0
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            linenum += 1
        file.close()
        return linenum


def read_inputs(input_file, wait=0.5):
    import __main__
    global endinput
    maxlines = getmaxlines(input_file)
    endinput = False
    ord = getattr(__main__, 'ord', None)
    file = open(input_file, 'r', encoding="utf-8", errors='ignore')
    
    content = file.readlines()
    
    ord.start_ord()

    for input in content:
        if endinput:
            break
        ord.make_input(input.strip())
        if not wait == 0:
            time.sleep(wait)
    file.close()
    ord.run_eom()

    return True
    