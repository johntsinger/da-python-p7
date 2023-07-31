# Python Application Developer - P7 -Solve problems using Python algorithms

## Description

Implementation of algorithms to find the best combination of shares to buy, to obtain the best profit after 2 years :
  - bruteforce algorithm
  - knapsack algorithm

## Installation guide

### Clone repository with Git :

    git clone https://github.com/johntsinger/da-python-p7.git
    
or

### Download the repository :

- On the [project page](https://github.com/johntsinger/da-python-p7)
- Click on green Code button
- Click on download ZIP
- Extract the file.

### Install Python :

If you don't have Python 3, please visit : https://www.python.org/downloads/ to download it !

### Virtual Environment :

#### Create a virtual environment in the project root :

    python -m venv env

#### Activate a virtual environment :

##### windows :

    env/Scripts/activate
    
##### linux/mac :

    source env/bin/activate
    
#### Install dependencies :

    pip install -r requirements.txt

## Run the program :

### Arguments :

  - -f --file : the name of the file to be opened without extension. (default=shares)
    - Can be : shares, dataset1, dataset2
  - -i --invest : the investment amount. (default=500)
    - Must be an integer

### Bruteforce :

    python bruteforce.py [-f FILE] [-i INVEST]

**DO NOT USE with dataset1 or dataset2 this can be extremely long and saturate your RAM**

### Optimised :

    python optimized.py [-f FILE] [-i INVEST]

## Contact :
Jonathan Singer - john.t.singer@gmail.com\
Project link : https://github.com/johntsinger/da-python-p7
