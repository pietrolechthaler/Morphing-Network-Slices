#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
                   +-------+
           +-------> Main  |
           |       +---+---+
           |           |
           |           |
           |   +-------v-------+
 Events----+   | NetController <---------Topologies
 - user        +-------+-------+
 - timers              |
                       |            +--->Hosts
               +-------v-------+    |
               |TopoController +----+
               +---------------+    |
                                    +--->Switches
'''

from netController import *

if __name__ == "__main__":

    setLogLevel("info")

    netController = NetController(4)

    netController.start()

    netController.test()

    info(str(dir(netController.net.switches[0])))

    netController.stop()