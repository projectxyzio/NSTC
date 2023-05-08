#!/bin/bash

echo -e "Checking System\n"
# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is already installed"
else
    # Install Python 3
    if [[ $(uname) == "Linux" ]]; then
        apt-get update
        apt-get install python3
    elif [[ $(uname) == "Darwin" ]]; then
        brew install python3
    fi
fi

# Check if pip3 is available
if ! command -v pip3 &> /dev/null
then
    # Install pip3
    echo "Pip3 is not available. Installing pip3..."
    if [[ "$(uname)" == "Darwin" ]]; then
        # For Mac
        brew install python3
    else
        # For Linux
        apt-get update &&  apt-get -y install python3-pip
    fi
else
    echo "Pip3 is already installed."
fi


#Installing python module  - virtualenv
pip3 install virtualenv &>/dev/null

#Creating Python Virtaul ENV 
echo "Creating  Python Virtaul ENV "
python3  -m virtualenv env3 &>/dev/null 
source env3/bin/activate 
pip3 install -r requirements.txt &>/dev/null
deactivate 
echo "All Required  Python Packages Installed"


echo -e  " \n Activate python virtaul env before running the scripts by  running :  source env3/bin/activate "
