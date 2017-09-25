# Lab for class of Network Security


### Instructions on start.sh

1. pg
    1. install  
    `./start.sh pg i` will install the playground dependencies.
    2. upgrade
    `./start sh pg u` will upgrade the playground dependencies.

2. run
    1. test
    `./start.sh run test 1b` will run submission file in lab 1b. Up to now, you can only run 1b or 1c.
    2. server
    `./start.sh run server` will run a Lab 1 server which listen at ('4.5.3.9596', 101).
    3. client
    `./start.sh run client mode` will run a Lab 1 client which connect to (mode, 101). The default value of mode is '4.5.3.9596'.

---

My environment:  
- macOS Sierra 10.12.6
- python 3.6.2

All the submission tests have been passed.

To run the code, you should:  

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

4. **According to instructions on shell script, run the code.**