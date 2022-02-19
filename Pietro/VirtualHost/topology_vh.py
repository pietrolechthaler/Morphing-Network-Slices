#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from comnetsemu.node import DockerHost
from comnetsemu.net import Containernet


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
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(4):
            self.addHost("h%d" % (i + 1), **host_config)

        #Add Docker hosts 
        self.addDockerHost("dh1", dimage="openvswitch/ovs:2.11.2_debian", ip="10.0.0.10/24")
        self.addDockerHost("dh2", dimage="openvswitch/ovs:2.11.2_debian", ip="10.0.0.11/24")
        
        
        # Add switch links
        self.addLink("s1", "s2", **http_link_config)
        self.addLink("s2", "s3", **http_link_config)
        self.addLink("s3", "s4", **http_link_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s2", **host_link_config)
        self.addLink("h3", "s3", **host_link_config)
        self.addLink("h4", "s4", **host_link_config)

        #add Dockerhost links
        self.addLink("dh1", "s1", **host_link_config)
        self.addLink("dh1", "s3", **host_link_config)
        self.addLink("dh2", "s4", **host_link_config)
        self.addLink("dh2", "s1", **host_link_config)




topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__":
    topo = NetworkSlicingTopo()
    net = Containernet(
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
