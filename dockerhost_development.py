#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
About: Basic example of using Docker as a Mininet host.
       Like upstream Mininet, the network topology can be either created by
       provide a topology class or directly using the network object.

Topo: Two Docker hosts (h1, h2) connected directly to a single switch (s1).

Tests:
- Iperf UDP bandwidth test between h1 and h2.
- Packet losses test with ping and increased link loss rate.
"""

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge, OVSKernelSwitch
from mininet.topo import Topo
from mininet.cli import CLI

PING_COUNT = 15

class TestTopo(Topo):
    def build(self, n):
        switch = self.addSwitch("s1")
        for h in range(1, n + 1):
            host = self.addHost(
                "h%s" % h,
                cls=DockerHost,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
            )
            self.addLink(switch, host, bw=10, delay="100ms")

class EmptyTopo(Topo):
    def build(self):
        pass


def add_host(net, index):
    return net.addHost(
        "h" + str(index),
        cls=DockerHost,
        dimage="dev_test",
        ip="10.0.0." + str(index) + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
    )

def create_topo(net):
    info("\t adding switches...\n")
    net.addSwitch("s1")
    net.addSwitch("s2")
    net.addSwitch("s3")
    net.addSwitch("s4")

    info("\t adding hosts...\n")
    add_host(net, 1)
    add_host(net, 2)
    add_host(net, 3)
    add_host(net, 4)

    info("\t adding links (1/2)...\n")
    net.addLink("h1", "s1")
    net.addLink("h2", "s2")
    net.addLink("h3", "s3")
    net.addLink("h4", "s4")
    info("\t adding links (2/2)...\n")
    net.addLink("s1", "s2")
    net.addLink("s2", "s3")
    net.addLink("s3", "s4")

def extend_topo(net):
    info("\t adding switches...\n")
    net.addSwitch("s5")

    info("\t adding hosts...\n")
    add_host(net, 5)

    info("\t adding links (1/2)...\n")
    net.addLink("h5", "s5")
    info("\t adding links (2/2)...\n")
    net.addLink("s4", "s5")


if __name__ == "__main__":
    
    setLogLevel("info")

    info("[MAIN] Creating network\n")
    net = Containernet(controller=Controller, link=TCLink, switch=OVSBridge, topo=EmptyTopo(), build=False)
    create_topo(net)

    info("[MAIN] Starting network\n")
    net.build()
    net.start()
    #CLI(net)
    net.pingAll()

    #info("[MAIN] Stopping network\n")
    #net.stop()

    #info(str(dir(net)))

    info("[MAIN] Extending network\n")
    extend_topo(net)

    info("[MAIN] Starting network\n")
    net.build()
    net.start()
    net.pingAll()

    info("[MAIN] Stopping network\n")
    net.stop()
