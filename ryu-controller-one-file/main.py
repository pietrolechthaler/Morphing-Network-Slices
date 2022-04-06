#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


import os
import time
import subprocess
from netController import *

'''
main class for the "one file" solution based on the SDN controllers, topology and remote controller are launched autonomously.
The net obj. is then stopped and launched again with a different controller, when the user exits the CLI of the first example.
The physical topology remains the same but the logical one is changed thanks to the controller, inside the classes topo and net Controllers
there are methods for creating and morphing said physical topology, in this example we only show the string network creation.

The code of the controllers is the same as the example "controller-solution" the only difference is that this solution is launched with only one
file and cycles thruough the two istances.

'''

if __name__ == "__main__":

    setLogLevel("info")
    

    info("#### --- TOPOLOGIA A STRINGA --- ####\n")
    os.system('ryu-manager ./SDN/controller_string.py &') 
    netController = NetController(4, "string")
    netController.start()
    netController.CLI()
    netController.stop()

    print("\n Premere invio per la modalità ad anello")
    input()
    os.system('./clean.sh')             #script to clean the network with sudo mn -c, also closes active dockers since we initially used them

    info("\n\n#### --- TOPOLOGIA AD ANELLO --- ####\n")
    os.system('ryu-manager ./SDN/controller_ring.py &') 
    netController = NetController(4, "string")
    netController.start()
    netController.CLI()
    netController.stop()
    os.system('./clean.sh')