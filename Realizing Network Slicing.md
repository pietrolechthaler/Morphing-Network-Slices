# Morphing Network Slicing #
Authors: Ascari Giacomo, Gatti Matteo, Lechthaler Pietro

![Topology](topology.png).

## Short Introduction ##


```text
h1 ----                               ---- h3
      |  |--10Mbps-- s2 --10Mbps--|  |
      |  |                        |  |
       s1                          s4
      |  |                        |  |
      |  |--1Mbps--  s3  --1Mbps--|  |
h2 ----                               ---- h4
```

This repository contains the following folders:

1. network.py: Script to build a network with four hosts and four switches, bandwidth is 1Mbps and 10Mbps.

2. topology_slicing.py: Application to isolate the network topology into upper slice (h1 -> s1 -> s2 -> s4 -> h3, 10Mbps) and lower slice (h2 -> s1 -> s3 -> s4 -> h4, 1Mbps).

3. service_slicing.py: Application to isolate the service traffics into video traffic (UDP port 9999) obtaining 10Mbps and non-video traffic (the remaining services) obtaining 1Mbps.

## Task 1: Topology Slicing ##
The topology of network should be isolated into two slices:
1. Upper slice:
    ```text
    h1 ----                               ---- h3
          |  |--10Mbps-- s2 --10Mbps--|  |
          |  |                        |  |
           s1                          s4
    ```
2. Lower slice:
    ```text
           s1                          s4
          |  |                        |  |
          |  |--1Mbps--  s3  --1Mbps--|  |
    h2 ----                               ---- h4
    ```

### How to Run ###
You can simple run the emulation applications with following commands in ./app/network_slicing/.

1. Enabling Ryu controller to load the application and to run background:
    ```bash
    $ ryu-manager topology_slicing.py &
    ```
2. Starting the network with Mininet:
    ```bash
    $ sudo python3 network.py
    ```

Please stop the running Ryu controller before starting a new Ryu controller. For example, type `htop` in the terminal to show all running processes, press the key `F4` to look for the process *ryu-manager*, then press the key `F9` to stop the process, with the key `F10` to quite `htop`.

### How to verify ###
There are three modes to verify the slice:

1. ping mode: verifying connectivity, e.g.
    ```bash
    mininet> pingall
    *** Ping: testing ping reachability
    h1 -> X h3 X 
    h2 -> X X h4 
    h3 -> h1 X X 
    h4 -> X h2 X 
    *** Results: 66% dropped (4/12 received)
    ```

2. iperf mode: verifying bandwidth, e.g.
    ```bash
    mininet> iperf h1 h3
    *** Iperf: testing TCP bandwidth between h1 and h3 
    *** Results: ['9.50 Mbits/sec', '12.4 Mbits/sec']
    mininet> iperf h2 h4
    *** Iperf: testing TCP bandwidth between h2 and h4 
    *** Results: ['958 Kbits/sec', '1.76 Mbits/sec']
    ```

3. client mode: verifying flows on each switch, e.g.
    ```bash
    mininet> sh ovs-ofctl dump-flows s1
    ```

## Task 2: Service Slicing ##
The network should be isolated into two slices for two services:
1. Video traffic slice:
    The video traffic (UDP port 9999) is able to gain max. 10Mbps bandwidth. The right of video traffic to use it is not affected by other traffics.
2. Other traffic slice:
    All traffics, which are not type UDP port 9999, can use any path of the network, but must not affect video traffic.

### How to Run ###
You can simple run the emulation applications with following commands in ./app/network_slicing/.

1. Enabling Ryu controller to load each application and to run background:
    ```bash
    $ ryu-manager service_slicing.py &
    ```
2. Starting the network with Mininet:
    ```bash
    $ sudo python3 network.py
    ```

Please stop the running Ryu controller before starting a new Ryu controller. For example, type `htop` in the terminal to show all running processes, press the key `F4` to look for the process *ryu-manager*, then press the key `F9` to stop the process, with the key `F10` to quite `htop`.

## How to Verify ##
There are three modes to verify the slice:

1. ping mode: verifying connectivity, e.g.
    ```bash
    mininet> pingall
    *** Ping: testing ping reachability
    h1 -> h2 h3 h4 
    h2 -> h1 h3 h4 
    h3 -> h1 h2 h4 
    h4 -> h1 h2 h3 
    *** Results: 0% dropped (12/12 received)
    ```

2. iperf mode: verifying bandwidth, e.g.

    Video traffic from h1 to h3 (UDP connection with destination port 9999).

    Log on to h1 and h3 in new terminals:
        ```bash
        mininet> xterm h1 h3
        ```

    Start listening on the h3 as server:
        ```bash
        $ iperf -s -u -p 9999 -b 10M
        ```

    Start sending on the h1 as client:
        ```bash
        $ iperf -c 10.0.0.3 -u -p 9999 -b 10M -t 10 -i 1
        ```

3. client mode: verifying flows on each switch, e.g.
    ```bash
    mininet> sh ovs-ofctl dump-flows s1
    ```
