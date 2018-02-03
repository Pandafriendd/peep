# PEEP (Players Enjoy Eavesdropping Protocol)

### Introduction

PEEP is a TCP-like protocol for [Playground](https://github.com/CrimsonVista/Playground3) communication. PEEP implements most of the mechanisms in TCP like sequence number and ACK and it simplifies these mechanisms. PEEP is not a secure-level-layer protocol, so this repo also provides a PLS protocol to ensure the security.

### Installation

1. **Install virtualenv:**  
 `pip3 install virtualenv`  
   If there is only one version of Python in your machine and the Python version is already 3.0+, use pip instead.  

2. **Clone the repo:**  
 `git clone git@github.com:princessV/lab-for-netsec.git`

3. **Install playground dependencies in a virtual environment:**  
    `cd peep`
    `virtualenv --no-site-packages venv`  
    `source venv/bin/activate`  
    `./start.sh pg i`
