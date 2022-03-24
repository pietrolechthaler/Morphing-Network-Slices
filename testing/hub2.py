from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from _thread import start_new_thread
import os, stat
import json
import time
import csv
import requests
import sys


def four_switches_network():
    http_link_config = dict(bw=1)
    net = Mininet(topo=None,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink)
                   

    info('*** Add switches\n')
    h1 = net.addHost('h1', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04')

    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    net.addLink("h1", "s1")
    net.addLink("h2", "s2")
    net.addLink("s1", "h4")
    net.addLink("s2", "h4")

    info('*** Starting network\n')
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    net.build()
    h4.cmd("ifconfig h4-eth0 0")
    h4.cmd("ifconfig h4-eth1 0")
    h4.cmd("brctl addbr br0")
    h4.cmd("brctl addif br0 h4-eth0")
    h4.cmd("brctl addif br0 h4-eth1")
    #h4.cmd("brctl setageing br0
    h4.cmd("brctl addif br0 h4-eth2")
    h4.cmd("ifconfig br0 up")
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
four_switches_network()
