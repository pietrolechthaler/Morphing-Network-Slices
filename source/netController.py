#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from mininet.net import Mininet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

from topoController import *

def addVirtualHost(net, name, index):
    return net.addHost(
        name,
        cls=DockerHost,
        dimage="kathara/quagga:latest",
        ip="10.0.0." + str(index) + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
    )

def addHost(net,name,index):
    return net.addHost(
        name,
        ip="10.0.0." + str(index) + "/24",
    )

def addRouter(net,name,index):
    return net.addHost(
        name,
        ip="10.0." + str(index) + ".254/24"
    )
  
def addVirtualRouter(net,name,index):
    return net.addDocker(
        'r'+str(index),
        dimage="kathara/quagga:latest"
    )

def addHostR(net,name,index):
    return net.addHost(
        name,
        ip="10.0." + str(index) + ".1/24",
        mac="00:00:00:00:00:0"+str(index),
        defaultRoute='via 10.0.'+str(index)+'.254'
    )


def addVirtualSwitch(net,name,index):
    #definire anche come collegarlo?
    pass

class NetController():
    def __init__(self, count):
        info("[NC] instance init\n")
        self.net = Containernet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, topo=EmptyTopo(), build=False)
        self.count = count
        c0 = self.net.addController("c0")
        for i in range(0, count):
            host = addHostR(self.net, "h" + str(i+1), i+1)
            id = "r" + str(i+1)
            router = addRouter(self.net, id,i+1)
            
        
        self.topoController = TopoController()
        self.topoController.morph(self.net, "string",count)
        self.index = 0
        self.slic = SlicController()
        #self.net.build()
        #c0.start()
        #self.topoController.define_interfaces(self.net,4)
    
    def start(self):
        info("[NC] start\n")
        self.net.build()
        self.net.start()
        self.slic.morph(self.net, "string", "string", self.count)
        addVirtualHost(self.net,"r5",5)
        self.net["r5"].cmd("ifconfig r5-eth5 0")
        self.net["r4"].cmd("ifconfig r4-eth1 0")

        self.net.addLink(self.net.get("r4"), self.net.get("r5"),
                    intfName1="r4-eth1",
                    params1={'ip':'10.0.45.1/24'},
                    intfName2="r5-eth2",
                    params2={'ip':'10.0.45.2/24'}
        )
        #
        # self.net.addLink(self.net["r5"],self.net["r1"])
        #self.net["r5"].cmd

        self.test()
        #info("\n\n\n")
        #self.slic.morph2(self.net, "string", "string", self.count)

    '''def change(self):
        info("[NC] change\n")
        topologies = ["star", "ring", "string"]
        self.topoController.morph(self.net, topologies[self.index])
        self.index += 1
        self.net.build()
        self.net.start()'''

    def collapseSwitch(self,index):
        pass

    def deployVRouter(self):
        pass

    def deployDockerHost(self,index):
        info("[NC] deploy Docker Host\n")
        addVirtualHost(self.net,"h"+str(index),index)
        self.net.addLink("h"+str(index),"s4")


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

    def CLI(self):
        CLI(self.net)