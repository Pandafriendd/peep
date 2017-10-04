# Lab for class of Network Security

## Handshake examination instructions
1. Install
2. Make switch and vnic on:  
`cd /path/to/lab-for-netsec`  
`source venv/bin/activate`  
`pnetworking on`  
Check the pnetworking status, you should see a vnic called v_eth0 whose playground address is 26.1.22.9 has connected to a switch called switchpg1. The switch and vnic should all be enabled.
3. Start a server:  
`./start.sh run server`
4. Run another terminal in the same directory, start a client:  
`./start.sh run client`
5. Now you can see connection information printed on the terminal. I have already written some basic data transmission codes, so you can see all the information from handshake to Application layer messages.  
In server, you could find **'PEEP server received SYN'**, **'PEEP server sent SYN-ACK'**, and something like that. In client, you could see **'PEEP client sent SYN'** and something like that.


## Installation
Environment:  
- macOS Sierra 10.12.6
- python 3.6.2

1. **Install virtualenv:**  
 `pip3 install virtualenv`  
   If there is only one version of Python in your machine and the Python version is already 3.0+, use pip instead.  

2. **Clone the repo:**  
 `git clone git@github.com:princessV/lab-for-netsec.git`

3. **Install playground dependencies in a virtual environment:**  
    `cd lab-for-netsec`  
    `virtualenv --no-site-packages venv`  
    `source venv/bin/activate`  
    `./start.sh pg i`


## Instructions on start.sh
1. pg
    1. install
    `./start.sh pg i` will install the playground dependencies.
    2. upgrade
    `./start.sh pg u` will upgrade the playground dependencies.

2. run
    1. test
    `./start.sh run test arg` will run submission file in lab 1. Up to now, arg can be 1b or 1c.
    2. server
    `./start.sh run server` will run a server which listen at ('26.1.22.9', 101).
    3. client
    `./start.sh run client mode` will run a client which connect to (mode, 101). The default value of mode is '26.1.22.9'. 