#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


<<<<<<< Updated upstream
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
=======
def four_switches_network():
    http_link_config = dict(bw=1)
    net = Mininet(topo=None,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink)
                   
    # Create host nodes
    info('*** Add switches\n')
    h1 = net.addHost('h1', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02')
    h3 = net.addHost('h3', mac='00:00:00:00:00:03')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04')


    # Create switch nodes
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")
    s4 = net.addSwitch("s4")

    # Create virtual host nodes
    s5 = net.addSwitch("s5")
    s6 = net.addSwitch("s6")

    # Add host links
    net.addLink("h1", "s1")
    net.addLink("h2", "s2")
    net.addLink("h3", "s3")
    net.addLink("h4", "s4")
    
    # Add switch links
    net.addLink("s1", "s2")
    net.addLink("s2", "s3")
    net.addLink("s3", "s4")
    
    # Add virtual host links
    net.addLink("s1", "s5")
    net.addLink("s4", "s5")
    net.addLink("s1", "s6")
    net.addLink("s3", "s6")
>>>>>>> Stashed changes

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