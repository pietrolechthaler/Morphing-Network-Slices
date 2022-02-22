#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import RemoteController, Controller
    
    
if __name__ == "__main__":

    print("*** Creating the net")

    net = Containernet(controller=Controller, link=TCLink, xterms=False, autoSetMacs=False)
    mgr = VNFManager(net)
    host_config = dict(inNamespace=True)
    http_link_config = dict(bw=1)
    host_link_config = dict()

    print("*** Creating hosts node")
    for i in range(4):
        net.addHost("h%d" % (i + 1), **host_config)

    print("*** Creating DockerHosts")
    dh1 = net.addDockerHost(
            "dh1",
            dimage="dev_test",
            ip="127.0.0.1/24",
            docker_args={"hostname": "dh1"},
    )

    dh2 = net.addDockerHost(
            "dh2",
            dimage="dev_test",
            ip="127.0.0.1/24",
            docker_args={"hostname": "dh2"},
    )

    print("*** Creating switches")
    switch1 = net.addSwitch("s1")
    switch2 = net.addSwitch("s2")
    switch3 = net.addSwitch("s3")
    switch4 = net.addSwitch("s4")
    
    print("*** Creating links")    
    # Add switch links
    net.addLink("s1", "s2")
    net.addLink("s2", "s3")
    net.addLink("s3", "s4")

    # Add host links
    net.addLink("h1", "s1")
    net.addLink("h2", "s2")
    net.addLink("h3", "s3")
    net.addLink("h4", "s4")

    #Add DockerHost links
    net.addLink("dh1", "s1")
    net.addLink("dh1", "s4")
    net.addLink("dh2", "s2")
    net.addLink("dh2", "s3")
    
    print("*** Starting the network")
    net.start()
    
    
    print("*** Adding the Switch Container")
    dh1_container = mgr.addContainer(
            "dh1_container",
            "dh1",
            "openvswitch/ovs:2.11.2_debian",
            "docker run -itd --net=host --name=ovs-vswitchd --volumes-from=ovsdb-server --privileged openvswitch/ovs:2.11.2_debian ovs-vswitchd"
    )

    dh2_container = mgr.addContainer(
            "dh2_container",
            "dh2",
            "openvswitch/ovs:2.11.2_debian",
            "docker run -itd --net=host --name=ovs-vswitchd --volumes-from=ovsdb-server --privileged openvswitch/ovs:2.11.2_debian ovs-vswitchd"
    )
    print("*** Spawning XTerm")
    #spawnXtermDocker("dh1_container") --> non faceva nulla, rimosso
    print("*** Opening CLI")

    CLI(net)

    mgr.removeContainer(dh1_container.name)
    mgr.removeContainer(dh2_container.name)

    #non necessatio, mgr.stop ferma tutto da solo, ho letto dalla documentazione di
    #comnets: riga 112 di questo link:
    #https://git.comnets.net/public-repo/comnetsemu/-/blob/master/examples/dockerhost_manage_appcontainer.py
    
    #mgr.removeContainer("dh1_container")
    #mgr.removeContainer("dh2_container")
    #mgr.removeContainer("dh1")
    #mgr.removeContainer("dh2")


    net.stop()    
    mgr.stop()
