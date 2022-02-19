#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
DA RIFARE
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
    

    info("#### --- TOPOLOGIA A STRINGA --- ####\n")
    os.system('ryu-manager ./SDN\ controller/controller_string.py &') 
    netController = NetController(4, "string")
    netController.start()
    netController.CLI()
    netController.stop()

    print("\n Premere invio per la modalità ad anello")
    input()
    os.system('./clean.sh')

    info("\n\n#### --- TOPOLOGIA AD ANELLO --- ####\n")
    os.system('ryu-manager ./SDN\ controller/controller_ring.py &') 
    netController = NetController(4, "string")
    netController.start()
    netController.CLI()
    netController.stop()
    os.system('./clean.sh')