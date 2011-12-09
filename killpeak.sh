#!/bin/bash
if [ -a $1 ]
then
    for file in $1*
    do
        echo $file
        python killerpeak.py $file
    done
fi
echo "Don't forget delete directory rrd_bak if all is ok"
exit 0
