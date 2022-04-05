<p align="center">
  <a href="">
    <img src="https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices/blob/main/logo.png">
  </a>
  <h2 align="center">Morphing Network Slicing</h2>

  <p align="center">
    Softwarized and Virtualized Mobile Networks
  <br>
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

In this project the goal is to show how a topology can be dynamically changed using a RYU SND controller.

[inserire topologia e spiegazione della nostra idea]

<hr>

### Dowload

```
git clone https://github.com/pietrolechthaler/UniTn-MorphingNetworkSlices
```

<hr>

### Intallation

After downloading all the files and installing the [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu/-/tree/master) virtual emulator.

```
cd UniTn-MorphingNetworkSlices
```


<hr>

### Usage 

This repository contains the following folders which contain **four different implementations of the solution** and a **testing folder** with some ideas of possible solutions.

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
You can simple run the emulation applications with following commands in ./ryu-controller-one-file/SDN
Starting the network with an ad-hoc class created to deploy the net and the controller, using topology and slice controller classes:
```
$ sudo python3 main.py
```
There are several modes to verify the results:
1.  Flow table router: ``` $ mininet> sh ovs-ofctl dump-flows s1 ```
2.  

### Ryu-controller-solution

You can simple run the emulation applications with following commands in ./ryu-controller-solution/SDN

<br>Enabling Ryu controller to load the application and to run background:

```
$ ryu-manager controller_ring.py &
```
or in alternative:
```
$ ryu-manager controller_string.py &
```
Starting the network with Mininet:
```
$ sudo python3 topology.py
```

There are several modes to verify the results:
1.  Flow table router: ``` $ mininet> sh ovs-ofctl dump-flows s1 ```
2.  


### Ryu-controller-one-file
You can simple run the emulation applications with following commands in ./ryu-controller-one-file/SDN
Starting the network with an ad-hoc class created to deploy the net and the controller, using topology and slice controller classes:
```
$ sudo python3 main.py
```
There are several modes to verify the results:
1.  Flow table router: ``` $ mininet> sh ovs-ofctl dump-flows s1 ```
2.  

### Virtual-host-solution
You can simply run the emulation applications with following commands in ./ryu-controller-router/SDN
Enabling Ryu controller to load the application and to run background:
```
$ ryu-manager controller_ring.py &
```
or in alternative:
```
$ ryu-manager controller_string.py &
```
Starting the network with Mininet:
```
$ sudo python3 topology.py
```
There are several modes to verify the results:
1.  Flow table router: ``` $ mininet> sh ovs-ofctl dump-flows s1 ```
2.  

<hr>

### Contributors
* [Ascari Giacomo](https://github.com/giacomo-ascari)
* [Gatti Matteo](https://github.com/matteo-gatti)
* [Lechthaler Pietro](https://github.com/pietrolechthaler)
