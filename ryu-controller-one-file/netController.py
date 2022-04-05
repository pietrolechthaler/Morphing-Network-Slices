#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from mininet.net import Mininet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch, RemoteController
from mininet.topo import Topo
from mininet.cli import CLI

from topoController import *

#method to add a virtual host to the net
def addVirtualHost(net, name, index):
    return net.addHost(
        name,
        cls=DockerHost,
        dimage="dev_test",
        ip="10.0.0." + str(index) + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
    )
#method to add a classic host to the net
def addHost(net,name,index):
    return net.addHost(
        name,
        ip="10.0.0." + str(index) + "/24",
        mac="00:00:00:00:00:0"+ str(index),
    )

class NetController():
    #topology param is the actual physical topology we want, string or ring
    def __init__(self, count, topology):
        info("[NC] instance init\n")
        self.net = Mininet(controller=RemoteController, 
        link=TCLink, switch=OVSKernelSwitch, topo=EmptyTopo(), 
        build=False,autoSetMacs=True,   #for some reason this was very important for the network to work!
        autoStaticArp=True)
        
        for i in range(0, count):
            addHost(self.net, "h" + str(i+1), i+1)
            self.net.addSwitch("s" + str(i+1))
        
        self.topoController = TopoController()
        self.topoController.morph(self.net, topology)   #topology controller will had the correct links
        self.index = 0

    #method to start the net
    def start(self):
        info("[NC] start\n")
        self.net.build()
        self.net.start()

    #method to change topology, cycling through the list: star,ring,string
    def change(self):
        info("[NC] change\n")
        topologies = ["star", "ring", "string"]
        self.topoController.morph(self.net, topologies[self.index])
        self.index += 1
        self.net.build()
        self.net.start()

    #deploy method, unused since we couldn't benefit from "deploying" from the controller
    def deployDockerHost(self,index,router):
        info("[NC] deploy Docker Host\n")
        addVirtualHost(self.net,"h"+str(index),index)
        self.net.addLink("h"+str(index),router)

    #method to stop the network
    def stop(self):
        info("[NC] stop\n")
        self.net.stop()
    
    #debug print
    def print(self):
        info("Controllers: " + str(self.net.controllers) + "\n")
        info("Hosts: " + str(self.net.hosts) + "\n")
        info("Links: " + str(self.net.links) + "\n")
        info("Switches: " + str(self.net.switches) + "\n")

    def test(self):
        self.net.pingAll()

    def CLI(self):
        CLI(self.net)