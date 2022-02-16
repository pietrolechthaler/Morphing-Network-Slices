#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

from topoController import *

def addHost(net, name, index):
    return net.addHost(
        name,
        cls=DockerHost,
        dimage="dev_test",
        ip="10.0.0." + str(index) + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
    )

class NetController():
    def __init__(self, count):
        info("[NC] instance init\n")
        self.net = Containernet(controller=Controller, link=TCLink, switch=OVSBridge, topo=EmptyTopo(), build=False)
        
        self.net.addController("c0")
        for i in range(0, count):
            addHost(self.net, "h" + str(i+1), i+1)
            self.net.addSwitch("s" + str(i+1))
        
        self.topoController = TopoController()
        self.topoController.morph(self.net, "string")
        self.index = 0

    def start(self):
        info("[NC] start\n")
        self.net.build()
        self.net.start()
    
    def change(self):
        info("[NC] change\n")
        topologies = ["star", "ring", "string"]
        self.topoController.morph(self.net, topologies[self.index])
        self.index += 1
        self.net.build()
        self.net.start()

    def stop(self):
        info("[NC] stop\n")
        self.net.stop()
    
    def print(self):
        info("Controllers: " + str(self.net.controllers) + "\n")
        info("Hosts: " + str(self.net.hosts) + "\n")
        info("Links: " + str(self.net.links) + "\n")
        info("Switches: " + str(self.net.switches) + "\n")

    def test(self):
        self.net.pingAll()
