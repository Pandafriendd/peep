# Lab for class of Network Security


**Please do not run the codes by entering the lab dir and run: `python submission.py`, which would cause a *ModuleNotFound* error**  

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
    `pip install git+https://github.com/CrimsonVista/Playground3.git@master`  

4. **Run the unit test:**  
    `./start.sh [args]`  
   Up to now the args = [1b, 1c]    
   If your OS does not support .sh. You should use full module path like `python -m netsec_fall2017.lab_1c.submission` instead.
