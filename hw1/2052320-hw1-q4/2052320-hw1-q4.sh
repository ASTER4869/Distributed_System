#!/bin/bash


counts=0
read -p "please input seconds:" counts
for((time=$counts;time>=0;time--))
do
    if((($counts-$time)%10==0))
    then
        echo $time
    fi
    sleep 1
done