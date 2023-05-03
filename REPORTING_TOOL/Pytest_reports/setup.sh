#!/bin/bash

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

pip3 install virtualenv

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
python3  -m virtualenv env3 &>/dev/null
source env3/bin/activate 
pip3 install -r requirements.txt &>/dev/null 
deactivate 
echo "All Required  Python Packages Installed"


# Check if Allure is installed
if command -v allure &>/dev/null; then
    echo "Allure is already installed"
else
    # Install Allure
    if [[ $(uname) == "Linux" ]]; then

        apt-get update
        apt-get install allure
    elif [[ $(uname) == "Darwin" ]]; then
        if ! command -v brew &> /dev/null
        then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            echo "Homebrew is already installed."
        fi
        brew install allure

    fi
fi

echo -e " \n Activate python virtaul env with :  source env3/bin/activate "
