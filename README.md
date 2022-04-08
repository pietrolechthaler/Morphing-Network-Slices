<p align="center">
  <a href="">
    <img src="https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices/blob/main/logo.png">
  </a>
  <h2 align="center">Morphing Network Slicing</h2>

  <p align="center">
  Exam project for Softwarized and Virtualized Mobile Networks 
  <br>University of Trento - Prof. <a href="https://www.granelli-lab.org/staff/fabrizio-granelli">Fabrizio Granelli</a>
  </p>
</p>
<br>

## Table of contents
- [Description](#description)
- [Download](#dowload)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)

<hr>

### Description


<a href="">
<img src="https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices/blob/main/topology.png">
</a>

In this project the goal is to show how a topology can be dynamically changed using a RYU SDN controller.
We use the same underlying topology, as shown in the picture, to demonstrate that RYU SDN Controllers can also be used to morph the logical view of the slice.
For clarity we use the same topologies, both physical and logical in all of our examples and test cases, so that the focus can be drawn to the proof of concept of the slice morphing and not on the topology itself.

Only one example "cheats" this rule by adding new devices, but is well documented in the topology file itself of the virtual host solution.
Furthermore, all the changes in topology are static since we encountered some major issues with the flow tables in mininet, forcing us this way (the router solution, since it doesn't use flow tables but routing tables, works dynamically instead), this and other issues are well documented in the related files.

<hr>

### Download

```
git clone https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices
```

<hr>

### Installation

After downloading all the files and installing the [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu/-/tree/master) virtual emulator.

```
cd UniTn-MorphingNetworkSlices
```


<hr>

### Usage 

This repository contains the following folders which contain **four different implementations of the solution** and a **[testing folder](https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices/tree/main/testing)** with some ideas of possible solutions.

```
UniTn-MorphingNetworkSlices
├── routing-tables-solution
├── ryu-controller-solution
├── ryu-controller-one-file
├── virtual-host-solution
├── testing
```
<hr>

### Routing-tables-solution ###
You can simply run the emulation applications with following commands in ./ryu-controller-one-file
<br>Starting the network with an ad-hoc class created to deploy the net and the controller, using topology and slice controller classes:
```
$ cd routing-tables-solution
$ sudo python3 main.py
```
There are several modes to verify the results:
1.  Flow table router: ```  mininet> r1 ip route ```
2.  Try ping all: ```  mininet> pingall ```
3.  Flow dump: ```  mininet> dump flows ```

### Ryu-controller-solution

You can simple run the emulation applications with following commands in ./ryu-controller-solution/SDN
<br>Enabling Ryu controller to load the application and to run background:

```
$ cd ryu-controller-solution/SDN
$ ryu-manager controller_ring.py &
```
or in alternative:
```
$ cd ryu-controller-solution/SDN
$ ryu-manager controller_string.py &
```
Starting the network with Mininet:
```
$ cd ryu-controller-solution
$ sudo python3 topology.py
```

There are several modes to verify the results:
1.  Flow table router: ``` $:sudo ovs-ofctl dump-flows s1 ```
2.  try ping all:  ```  mininet> pingall``` : this should work fine with string topology and show an X when reaching H2 in ring topology (since we excluded that Switch)


### Ryu-controller-one-file
You can simple run the emulation applications with following commands in ./ryu-controller-one-file/
<br>Starting the network with an ad-hoc class created to deploy the net and the controller, using topology and slice controller classes:
```
$ cd ryu-controller-one-file
$ sudo python3 main.py
```

To verify, try ping all:  ```  mininet> pingall``` 

this should work fine with string topology and show an X when reaching H2 in ring topology (since we excluded that Switch).

Since this example is running on one file only, after exiting the first example you'll go to the second one and the pingall comand should work differently!

### Virtual-host-solution
You can simply run the emulation applications with following commands in ./virtual-host-solution/
<br>Enabling Ryu controller to load the application and to run background:
<br>
```
$ cd Virtual-host-solution/SDN
$ ryu-manager controller.py &
```
Starting the network with Mininet:
```
$ cd Virtual-host-solution
$ sudo python3 topology.py
```
There are several modes to verify the results:
1.  Flow table router: ``` $:sudo ovs-ofctl dump-flows s1 ```
2.  try ping all:  ```  mininet> pingall``` : this should work fine with string topology and show an X when reaching H2 in ring topology (since we excluded that Switch)
<hr>

### Contributors
* [Ascari Giacomo](https://github.com/giacomo-ascari)
* [Gatti Matteo](https://github.com/matteo-gatti)
* [Lechthaler Pietro](https://github.com/pietrolechthaler)
