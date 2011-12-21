#!/bin/bash
param=($@)
if [ -a $1 ]
then
    for file in $1*
    do
        echo $file
        python killerpeak.py $file ${param[@]:1} # Все эелементы массива, начиная со 2-го
    done
fi
echo "Don't forget delete directory rrd_bak if all is ok"
exit 0
