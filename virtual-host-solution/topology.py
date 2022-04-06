#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


class NetworkSlicingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        http_link_config = dict(bw=1)
        host_link_config = dict()

        # Create switch nodes
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        self.addHost('h1', mac='00:00:00:00:00:01')
        self.addHost('h2', mac='00:00:00:00:00:02')
        self.addHost('h3', mac='00:00:00:00:00:03')
        self.addHost('h4', mac='00:00:00:00:00:04')
        
        #Create virtual host
        self.addSwitch("s5")
        self.addSwitch("s6")

        #Add switch links
        self.addLink("h1", "s1")
        self.addLink("h2", "s2")
        self.addLink("h3", "s3")
        self.addLink("h4", "s4")

        #Add host links
        self.addLink("s1", "s2")
        self.addLink("s2", "s3")
        self.addLink("s3", "s4")
        
        #Add virtual host links
        self.addLink("s1", "s5")
        self.addLink("s4", "s5")
        self.addLink("s1", "s6")
        self.addLink("s3", "s6")


topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__":
    topo = NetworkSlicingTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()