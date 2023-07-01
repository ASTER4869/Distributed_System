#!/bin/bash

analysis_log()
{
    file="2052320-hw1-q2.log"
    

    echo $(wc -l < $file)
    echo $(wc -m < $file)



    first_line=(`head -n 1 $file`)
    last_line=(`tail -n 1 $file`)
    start_time=${first_line[0]}
    end_time=${last_line[0]}

    time=$(($(date +%s -d "2022-09-01 $end_time") - $(date +%s -d "2022-09-01 $start_time")))
    echo $time

    num_array=(0 0 0)
    num=0
    while IFS=", " read -a line
    do
        num_array[0]=$(printf "%.2f" `echo "scale=2;${num_array[0]}+${line[-1]}" | bc`)

        num_array[1]=$(printf "%.2f" `echo "scale=2;${num_array[1]}+${line[-2]}" | bc`)
        num_array[2]=$(printf "%.2f" `echo "scale=2;${num_array[2]}+${line[-3]}" | bc`)
        num=$((num+1))
    done < $file
    if(($num != 0))
    then
        for((i=0; i<=2;i++))
        do
            printf "%.2f " `echo "scale=2;${num_array[$i]}/$num" | bc`
        done
        printf "\n"
    else
        echo 0 
    fi
}

analysis_log > 2052320-hw1-q3.log