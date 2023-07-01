#!/bin/bash

print_uptime()
{
    for((i=0; i<=15;i++))
    do
        uptime
        sleep 10s
    done
}

print_uptime >> 2052320-hw1-q2.log