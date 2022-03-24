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
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host)
    h2 = net.addHost('h2', cls=Host)
    h3 = net.addHost('h3', cls=Host)
    h4 = net.addHost('h4', cls=Host)
    h5 = net.addHost('h5', cls=Host)

    info('*** Add links\n')
    net.addLink(s1, s2, **http_link_config)
    net.addLink(s2, s3, **http_link_config)
    net.addLink(s3, s4, **http_link_config)

    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(h5, s4)
    net.addLink(h5, s1)

    info('*** Starting network\n')
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    time.sleep(3)
    h5.cmd("ifconfig h5-eth0 0")
    h5.cmd("ifconfig h5-eth1 0")
    h5.cmd("brctl addbr br0")
    h5.cmd("brctl addif br0 h5-eth0")
    h5.cmd("brctl addif br0 h5-eth1")
    #h4.cmd("brctl setageing br0 0")
    h5.cmd("ifconfig br0 up")
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
four_switches_network()
