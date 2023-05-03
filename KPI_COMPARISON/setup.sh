#!/bin/bash

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is already installed"
else
    # Install Python 3
    if [[ $(uname) == "Linux" ]]; then
        sudo apt-get update
        sudo apt-get install python3
    elif [[ $(uname) == "Darwin" ]]; then
        brew install python3
    fi
fi

# Check if pip3 is available
if ! command -v pip3 &> /dev/null
then
    # Install pip3
    echo "pip3 is not available. Installing pip3..."
    if [[ "$(uname)" == "Darwin" ]]; then
        # For Mac
        brew install python3
    else
        # For Linux
        apt-get update &&  apt-get -y install python3-pip
    fi
else
    echo "pip3 is already installed."
fi


#Installing python module  - virtualenv
pip3 install virtualenv

#Creating Python Virtaul ENV 
echo "Creating  Python Virtaul ENV "
python3  -m virtualenv env3
source env3/bin/activate 
pip3 install -r requirements.txt &>/dev/null; 
deactivate 

echo "Activate python virtaul env with :  source env3/bin/activate "
