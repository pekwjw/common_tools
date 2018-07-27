#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import sys
import os
import time
import getopt

def drawPicCpuMem(memtime,memdata,cputime,cpudata,pid=0,start=""):
    outpng = str(pid) + "_mem_cpu_record.png"
    plt.figure(figsize = (16,10))
    plt.subplot(211) 
    plt.plot(memtime,memdata,"r-",linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Memory(G)")
    plt.xlim(0,memtime[-1]*1.1)
    plt.grid()
    plt.title("Memory Use Stat of Pid:" + str(pid) + ", Begin from:" + str(start))
    
    plt.subplot(212)
    plt.plot(cputime,cpudata,"b--",linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Cpu Usage Percent")
    plt.xlim(0,cputime[-1]*1.1)
    plt.grid()
    plt.title("Cpu Usage Percent of Pid:" + str(pid) + ", Begin from:" + str(start))
    plt.savefig(outpng) 

def getDataFromFile(datafile):
    res = []
    fo = open(datafile,'r')
    line = fo.readline()
    while line:
        res.append(float(line.strip("\n").split(" ")[3]))
        line = fo.readline()
    length = len(res)
    timedata = range(0,length*5,5)
    return timedata,res

def getArgv(argv):
    try: 
        opts,args = getopt.getopt(argv,"hp:t:",["pid=","starttime="])
    except getopt.GetoptError:
        print "python genCpuMemPic.py -p <pid> -t <starttimestamp> "
        sys.exit(2)
    for opt,arg in opts:
        if opt == "-h":
            print "python genCpuMemPic.py -p <pid> -t <starttimestamp>"
            sys.exit()
        elif opt in ("-p","--pid"):
            global pid 
            pid = int(arg)
        elif opt in ("-t","--starttime"):
            global start 
            start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(arg)))
    
if __name__ == "__main__":
    getArgv(sys.argv[1:])
    abspath = os.path.abspath(".")
    memFile = abspath + "/recordpath/memory"
    cpuFile = abspath + "/recordpath/cpuper"
    memtime,memdata = getDataFromFile(memFile)
    cputime,cpudata = getDataFromFile(cpuFile)
    drawPicCpuMem(memtime,memdata,cputime,cpudata,pid,start)
