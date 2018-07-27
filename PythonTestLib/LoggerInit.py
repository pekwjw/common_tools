# -*- coding:utf-8 -*-

import logging
import os
import commands

def setup_common_logger(lname,lpath='',llevel=logging.INFO,lfmt='%(asctime)s %(lineno)d %(levelname)s: %(message)s'):
    """Init an available log handler according the input args.
    Args:
        lname: str
            module name.
        lpath: str
            the log file path, default value is the os.path.abspath(__file__)+"/log/".
        llevel: log level 
            default value is "logging.INFO",optional value are "logging.DEBUG","logging.INFO","logging.WARNING","logging.ERROR","logging.CRITICAL"
        lfmt: str
            the log format, default value is "%(asctime)s %(lineno)d %(levelname)s: %(message)s".
         
    Returns:
        lhandler , an available log handler 
    """
    logpath = lpath if lpath else os.path.abspath(__file__)+"/../log/"
    try:
        if os.path.exists(logpath):
            pass
        else:
            commands.getstatusoutput("mkdir -p "+logpath)
    except Exception,err:
        print "ERROR: Access to logpath failed!"
        os._exit(1)
    logname = lpath + lname + ".log"
    lhandler = logging.getLogger(lname)
    fmt = logging.Formatter(lfmt)
    file_handler = logging.FileHandler(logname)
    file_handler.setFormatter(fmt)
    lhandler.addHandler(file_handler)
    lhandler.setLevel(llevel)
    return lhandler

def main():
    pass

if __name__ == "__main__":
    main()

