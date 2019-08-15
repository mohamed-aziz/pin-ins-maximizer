from multiprocessing import Pool
from collections import deque
import subprocess
import re
import string
import sys

pin_binary = "/home/mo/pin/pin"
inscount_library = "/home/mo/pin/source/tools/ManualExamples/obj-ia32/inscount0.so"
binary = '/home/mo/a.out'

rule = re.compile(b"Count (\d*)")

flag = ""
flag_length = 100 
flag_range = string.printable 

def execute_command(stdin):
    print(stdin)
    out = subprocess.Popen(('echo', stdin), stdout=subprocess.PIPE)
    output = subprocess.Popen((pin_binary, '-t', inscount_library, '-o', '/dev/stdout', '--', binary), 
            stdin=out.stdout, stdout=subprocess.PIPE)
    out.wait()
    retval = output.communicate()[0]
    return int(rule.match(retval).group(1))
    
if __name__ == "__main__":
    num_procs = int(sys.argv[1])
    with Pool(num_procs) as p:
        for i in range(flag_length):            
            inpu = [flag + char + ("A" * (flag_length - len(flag)))  for char in flag_range]
            result = deque(p.imap(execute_command, inpu))
            mc =  max(flag_range, key=lambda x: result[flag_range.index(x)])
            for i, elem in enumerate(result):
                print(inpu[i], ":", elem)
            print("Using char =", mc)
            flag += mc
            print("Current flag:", flag)
