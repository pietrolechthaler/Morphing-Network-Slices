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

### Docker

This solutions demonstrates how to use a docker image of a [OVS Switch](https://hub.docker.com/r/openvswitch/ovs) inside Dockerhost instance.
The Dockerhost with internal Docker containers deployed is used to simulate an OVS Switch. 
We wanted to use this technique to deploy "virtual hosts" inside the network but we soon realized that it was not working properly, and while we were able to make the img work, getting the controller to recognize the docker as a true switch inside the network was way too complex for us.
So we decided to use actual real switches to demonstrate what we could have done with this virtual solution if only we were able to "crack" this detail.

<hr>

### Hub

This solutions demonstrates how to use an Host acting like an L2 non-learning hub, simply forwarding packets from one port to the other.
This was our base for the "virtual - host" solution until we realized that hubs tend to work in a way that is too dumb for our aims in this project and more than once we had problems with them with code that worked fine on switches.
We then decided to cut this solution and to replace them with switches, making it work like intended. The code is still available here in /Hub, for testing and completeness purposes


