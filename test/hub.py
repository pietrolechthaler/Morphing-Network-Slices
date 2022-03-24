#!/usr/bin/env python

from mininet.cli import CLI
from mininet.link import Link,TCLink,Intf
from mininet.net import Mininet
from mininet.node import RemoteController

 

if '__main__' == __name__:

  net = Mininet(link=TCLink)
  h1 = net.addHost('h1', mac='00:00:00:00:01:00')
  h2 = net.addHost('h2', mac='00:00:00:00:02:00')
  h3 = net.addHost('h3', mac='00:00:00:00:03:00')
  h4 = net.addHost('h4', mac='00:00:00:00:04:00')

  s1 = net.addSwitch("s1")
  s2 = net.addSwitch("s2")
  s3 = net.addSwitch("s3")

  net.addLink("h1", "s1")
  net.addLink("h2", "s2")
  net.addLink("h3", "s3")
  net.addLink("s1", "h4")
  net.addLink("s2", "h4")
  net.addLink("s3", "h4")

  net.build()
  h4.cmd("ifconfig h4-eth0 0")
  h4.cmd("ifconfig h4-eth1 0")
  h4.cmd("ifconfig h4-eth2 0")
  h4.cmd("brctl addbr br0")
  h4.cmd("brctl addif br0 h4-eth0")
  h4.cmd("brctl addif br0 h4-eth1")
  #h4.cmd("brctl setageing br0 0")
  h4.cmd("brctl addif br0 h4-eth2")
  h4.cmd("ifconfig br0 up")
  CLI(net)
  net.stop()