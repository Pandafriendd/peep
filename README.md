# Lab for class of Network Security

### Content
- Lab 2 test instructions
- Installation
- Instructions on start.sh

---

### Lab 2 instructions
1. Install
2. Make switch and vnic on:  
`cd /path/to/lab-for-netsec`  
`source venv/bin/activate`  
`pnetworking on`  
Check the pnetworking status, you should see a vnic called v_eth0 whose playground address is 26.1.22.9 has connected to a unreliable_switch called switchpg2. The switch and vnic should all be enabled.
3. Rename the playground test module. Because the Python interpreter will identify a _test_ module as its built in module. So we go to `./venv/lib/site-packages/`, and find _test_ module, and then rename it, for example, _test1_.
4. Run the test command:  
`python -m test1.ThroughputTester client --reference-stack=lab2_protocol`
5. Now you can see a lot of messages are printed out. You should wait for several seconds and the record will be printed out after the session ends. In my environment, the run time is like:

| Run Time | Error Rate |
| :------: | :--------: |
|  20-25s  |  1/102400  |
| 1min40s  |  1/10240   |
| 3min30s  |   1/5000   |

(The run time will be increase by the increase of error rate. If you set the error more than 1/5000, the run time will be much longer. And there are chances the last packet will be missed.)

---

### Installation
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

---

### Instructions on start.sh
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