#!/bin/bash

isprime()
{
    if (($1 == 1))
    then
        return 0
    fi
    for ((i=2;i<=$1/2;i++))
    do
        if (($1%i == 0))
        then
            return 0
        fi
    done
    return 1
}

sum=0
for ((j=1; j<=100; j++))
do
    isprime $j
    if (($? == 1))
    then
        sum=$(($sum+$j))
    fi
done
echo $sum > 2052320-hw1-q1.log