#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:31:10 2024

@author: juanmeriles
"""
import threading


def print_thread_1():
    i = 0
    while True:
        i = i+1
        if i%6000 == 0:
            j = 1
            #print("Thread 1")


def print_even():
    for i in range(50):
        if  not i%2:
            print(i)


if __name__ =="__main__":
    t1 = threading.Thread(target=print_thread_1)
    t2 = threading.Thread(target=print_even)
    
    for i in range(2):
        if i==0:
            t1.start()
        if i ==1:
            t2.start()


    
    
    t1.join()
    t2.join()

    print("Done!")