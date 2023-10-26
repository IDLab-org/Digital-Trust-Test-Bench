#!/bin/bash

CHROME_DRIVER_VERSION='117.0.5938.149'
ALLURE_VERSION=2.24.0
# Install essentials if not installed
if ! command -v python3 &> /dev/null
then
    echo "Installing Python3..."
    sudo apt-get install -y python3
else
    echo "Python3 is already installed."
fi

if ! command -v pip3 &> /dev/null
then
    echo "Installing pip3..."
    sudo apt-get install -y python3-pip
else
    echo "pip3 is already installed."
fi

if ! command -v google-chrome &> /dev/null
then
    echo "Installing Google Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
else
    echo "Google Chrome is already installed. update to latest"
    sudo apt upgrade -y google-chrome-stable
fi

# Check and install Virtual Environment if not installed
if ! command -v virtualenv &> /dev/null
then
    echo "Installing Virtual Environment..."
    pip3 install virtualenv
else
    echo "Virtual Environment is already installed."
fi

# Create a directory for the project if it doesn't exist
PROJECT_DIR="tests"
if [ ! -d "$PROJECT_DIR" ]
then
    echo "Creating project directory..."
    mkdir "$PROJECT_DIR"
fi

# Install Python packages in the virtual environment if not installed
python3 -m pip install --upgrade pip
pip3 install selenium pytest allure-pytest

# Check and install ChromeDriver if not installed
if ! command -v chromedriver &> /dev/null
then
    echo "Installing ChromeDriver..."
    wget https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
    
    # Check if wget was successful
    if [ $? -ne 0 ]; then
        echo "Failed to download ChromeDriver."
        exit 1
    fi
    
    unzip chromedriver-linux64.zip
    
    # Check if unzip was successful
    if [ $? -ne 0 ]; then
        echo "Failed to extract ChromeDriver."
        exit 1
    fi
    
    sudo mv chromedriver /usr/local/bin/
    
    # Check if mv was successful
    if [ $? -ne 0 ]; then
        echo "Failed to move ChromeDriver."
        exit 1
    fi
    
    # Clean up
    rm chromedriver_linux64.zip
else
    echo "ChromeDriver is already installed."
fi

# Check if Java is installed
if ! command -v java &> /dev/null
then
    echo "Java is not installed. Installing..."
    sudo apt update
    sudo apt install -y openjdk-11-jdk
else
    echo "Java is already installed. Skipping..."
fi

# Check if Allure is installed and of the desired version
if command -v allure &> /dev/null
then
    INSTALLED_ALLURE_VERSION=$(sudo allure --version)
    if [ "$INSTALLED_ALLURE_VERSION" == "$ALLURE_VERSION" ]
    then
        echo "Allure $ALLURE_VERSION is already installed. Skipping..."
        exit 0
    else
        echo "Allure is installed but not the desired version. Updating..."
    fi
else
    echo "Allure is not installed. Installing..."
    wget https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure_${ALLURE_VERSION}-1_all.deb
    sudo dpkg -i allure_2.24.0-1_all.deb
fi

# Further steps...
echo "Environment setup complete."
