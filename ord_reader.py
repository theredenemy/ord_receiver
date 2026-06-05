import os
import time
import __main__

maindir = os.getcwd()
endinput = False
input_chain_on = True
can_do_input_chain = []
skip_in_list = []
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
    def input(self, input, input_chain=False):
        def wrapper(func):
            if input_chain:
                can_do_input_chain.append(input)
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
    
    def make_input(self, input, chain=1):
        if self.before_input_func:
            state = self.before_input_func()
            if state is False:
                return
        if input in self.registry:
            if input in can_do_input_chain:
                self.registry[input](chain)
            else:
                self.registry[input]()
        else:
            print(f"INVAILD INPUT : {input}")
            if self.invalid_func:
                self.invalid_func()
    def run_eom(self):
        if self.eom_func:
            self.eom_func()


# def get_pid(process_name):
#     pid = None
    
#     for proc in psutil.process_iter(['pid', 'name']):
#         if proc.info['name'].lower() == process_name.lower():
#             pid = proc.info['pid']
#             return pid

def getmaxlines(filename):
    linenum = 0
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            linenum += 1
        file.close()
        return linenum


def read_inputs(input_file, ord: OrdInput, wait=0.5):
    import threading
    global endinput
    maxlines = getmaxlines(input_file)
    lock = open("ord.lock", 'w')
    endinput = False
    #ord = getattr(__main__, 'ord', None)
    file = open(input_file, 'r', encoding="utf-8", errors='ignore')
    
    content = file.readlines()
    
    ord.start_ord()

    for i, input in enumerate(content):
        if i in skip_in_list:
            continue
        if endinput:
            break
        if input.strip() in can_do_input_chain and input_chain_on:
            chain_count = 1
            for line in range(maxlines - i):
                if not line + i + 1 >= len(content):
                    if content[line + i + 1].strip() == input.strip():
                        skip_in_list.append(line + i + 1)
                        chain_count += 1
                    else:
                        break
                else:
                    break
            ord.make_input(input.strip(), chain=chain_count)
        else:
            ord.make_input(input.strip())
        if not wait == 0:
            time.sleep(wait)
    file.close()
    ord.run_eom()
    lock.close()
    os.remove("ord.lock")

    return True
    