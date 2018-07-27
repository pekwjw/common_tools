#!/bin/sh
inteval=5
cur_time=`date +%s`
curpath=`pwd`

function getCPUstat
{
    pid=$1
    inteval=$2
    checknum=$3
    
    total_cpu_slice_1=`cat /proc/stat|grep "cpu "|awk '{for(i=2;i<=NF;i++)j+=$i;print j;}'`
    total_process_slice_1=`cat /proc/${pid}/stat|awk '{print $14+$15+$16+$17}'`
    for (( i=0;i<=${checknum};i++))
    do
        sleep $inteval 
        total_cpu_slice_2=`cat /proc/stat|grep "cpu "|awk '{for(i=2;i<=NF;i++)j+=$i;print j;}'`
        total_process_slice_2=`cat /proc/${pid}/stat|awk '{print $14+$15+$16+$17}'`
        cpu_usage=`echo "scale=2; 100 * ($total_process_slice_2 - $total_process_slice_1) / ($total_cpu_slice_2 - $total_cpu_slice_1)" |bc`

        #echo -e "$(date +"%y-%m-%d %H:%M:%S") cpu usage:$cpu_usage%"
        echo -e "[$(date +"%y-%m-%d %H:%M:%S")] cpu_usage: $cpu_usage %" >> ${curpath}/recordpath/cpuper
        vm=`cat /proc/$pid/status|grep -e VmRSS|awk '{print $2}'`
        #vmG=`echo "scale=2; $vm/1024.0/1024.0" |bc` 
        vmG=`echo "scale=2; $vm/1024.0/1024.0" |bc` 
        #echo -e "$(date +"%y-%m-%d %H:%M:%S") vmRss:${vmG}G"
        echo -e "[$(date +"%y-%m-%d %H:%M:%S")] vmRss: ${vmG} G" >> ${curpath}/recordpath/memory
        #write_db $cpu_usage ${vmG} ${pid}
    done
}

function checkMatplotlib(){
    res=`python -c "import matplotlib;print matplotlib.__file__"`
    if [ "${res}"x = ""x ] ; then 
        echo "PLEASE CHECK : Python Matplotlib cannot import correctly."
        echo "  Matplotlib install doc : http://km.oa.com/group/35175/docs/show/181413."
        exit 1
    fi
}     

function touchRecordFile(){
    if [ -d "${curpath}/recordpath/" ] ; then 
        rm -rf ${curpath}/recordpath/* 
    else
        mkdir ${curpath}/recordpath
    fi 

    if [ -f "${curpath}/recordpath/memory" ];then 
        > "${curpath}/recordpath/memory"
    else 
        touch "${curpath}/recordpath/memory"
    fi
    
    if [ -f "${curpath}/recordpath/cpuper" ];then 
        > "${curpath}/recordpath/cpuper"
    else 
        touch "${curpath}/recordpath/cpuper"
    fi
}

function main(){
    if [ $# == 1 ] ; then 
        pid=$1
        monitortime=1800
        checknum=$((360+5))
    elif [ $# == 2 ] ; then 
        pid=$1
        monitortime=$2
        checknum=$(($((${monitortime}/5))+5))
    else
        echo "USAGE: nohup sh $0 pid monitortime &      #pid:the process number;monitortime:the monitor time(s)"
        echo "    or nohup sh $0 pid & " 
        echo " e.g.: nohup sh stat_monitor.sh 123 3600 &  #this mean monitor the 123 process for 1 hour."
        echo "       nohup sh stat_monitor.sh 123 &     #this mean monitor the 123 process for 30 minutes."
        exit 1
    fi 
    
    checkMatplotlib
    touchRecordFile    
    getCPUstat ${pid} ${inteval} ${checknum}
    python genMemCpuPng.py -p ${pid} -t ${cur_time}
}

main $@
