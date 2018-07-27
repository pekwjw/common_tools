# -*- coding:utf-8 -*-

import time
from PythonTestLib import LoggerInit

global logcost 
logcost = LoggerInit.setup_common_logger("cost")

def timer(func):
    '''timer is a decorator ,which is used to measure the time cost of the function
    Args:
        func: str
            the function name 
    Returns:
        null
    Log:
        record the cost time in "cost.log" located in os.path.abspath(__file__), __file__ is the file where func is located in.
    '''
    def inner(*args):
        tbegin = time.time()
        func_res = func(*args)
        logcost.info(str(func.__name__) + " cost:" + str(int((time.time() - tbegin)*1000000)) + " us")
        return func_res
    return inner  

def main():
    pass

if __name__ == "__main__":
    main()
