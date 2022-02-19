#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
                   ┌───────┐
                   │ Main  │◄────── Events
                   └───┬───┘        - User
                       │            - Timers
                       ▼
               ┌───────────────┐
               │ NetController │
               └─┬───────────┬─┘
                 │           │
                 ▼           ▼
┌────────────────────┐   ┌───────────────────┐
│ TopologyController │   │ SlicingController │
└──────────┬─────────┘   └────────┬──────────┘
           │                      │
           │                      │
   Physical topology       Virtual topology
           │                      │
           │                      │
           │      ┌─────────┐     │
           └─────►│ Network │◄────┘
                  └─────────┘
 '''

import os
import time
import subprocess
from netController import *

if __name__ == "__main__":

    setLogLevel("info")
    ''''
    netController = NetController(4)

    netController.start()
    #netController.print()

    info("####CHANGE####\n")
    #netController.change()
    #netController.test()
    netController.deployDockerHost(5)
    netController.start()


    info("####TEST####\n")
    #info(str(dir(netController.net.switches[0])))    
    netController.test()
    netController.CLI()

    info("####CLEANUP####\n")
    os.system('sudo ./clean.sh') 
    #TODO: capire come mai non funziona la fermata di c0
    #netController.stop()
    '''
    #subprocess.call('ryu-manager line_slice_circle.py', shell=True) -->quando non ci saranno debug useremo questo sistema
    netController = NetController(4)
    netController.start()
    netController.CLI()
    netController.stop()