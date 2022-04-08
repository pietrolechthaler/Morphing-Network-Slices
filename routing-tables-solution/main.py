#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
                   ┌───────┐
                   │ Main  │◄────── Events
                   └───┬───┘        - Timers
                       |            - Users
                       │
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
 '''

import os
import time
from netController import *

if __name__ == "__main__":

    setLogLevel("info")

    # Inizializzazione NETCONTROLLER a 4 hosts
    netController = NetController(4)

    # Avvio NETCRONTROLLER
    netController.start()

    # Avvio istanza terminale al NETCONTROLLER
    netController.CLI()

    # Arresto NETCRONTROLLER
    netController.stop()
