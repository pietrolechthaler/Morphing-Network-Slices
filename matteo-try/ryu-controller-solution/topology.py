#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import time



class NetworkSlicingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        http_link_config = dict(bw=1)
        video_link_config = dict(bw=10)
        host_link_config = dict()

        # Create switch nodes
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        s3 = self.addSwitch("s3")
        s4 = self.addSwitch("s4")

        # Create host nodes
        h1 = self.addHost("h1", **host_config)
        h2 = self.addHost("h2", **host_config)
        h3 = self.addHost("h3", **host_config)
        h4 = self.addHost("h4", **host_config)
        h5 = self.addHost("h5", **host_config)
        # Add switch links
        self.addLink("s1", "s2", **http_link_config)
        self.addLink("s2", "s3", **http_link_config)
        self.addLink("s3", "s4", **http_link_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s2", **host_link_config)
        self.addLink("h3", "s3", **host_link_config)
        self.addLink("h4", "s4", **host_link_config)
        self.addLink("h5", "s4", **host_link_config)
        self.addLink("h5", "s1", **host_link_config)
        
        h5.cmd("ifconfig h5-eth0 0")
        h5.cmd("ifconfig h5-eth1 0")
        h5.cmd("ifconfig h5-eth2 0")
        h5.cmd("brctl addbr br0")
        h5.cmd("brctl addif br0 h5-eth0")
        h5.cmd("brctl addif br0 h5-eth1")
        #h4.cmd("brctl setageing br0 0")
        h5.cmd("brctl addif br0 h5-eth2")
        h5.cmd("ifconfig br0 up")


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
    time.sleep(3)
    CLI(net)
    net.stop()
