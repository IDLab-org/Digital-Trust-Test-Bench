#!/bin/bash

set -e  # Exit the script if any statement returns a non-true return value

CHROME_DRIVER_VERSION='117.0.5938.149'
ALLURE_VERSION=2.24.0

# Install essentials
apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
# Install Java 8
apt-get update && \
    apt-get install -y default-jdk

apt --fix-broken install

# Install Allure
wget https://github.com/allure-framework/allure2/releases/download/$ALLURE_VERSION/allure_$ALLURE_VERSION-1_all.deb
dpkg -i allure_$ALLURE_VERSION-1_all.deb
rm allure_$ALLURE_VERSION-1_all.deb

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Install Virtual Environment if not installed
pip3 install --upgrade pip
pip3 install virtualenv

# Create a directory for the project
PROJECT_DIR="tests"
mkdir -p "$PROJECT_DIR"

# Install Python packages
pip3 install selenium pytest allure-pytest

# Install ChromeDriver
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.149/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/
rm chromedriver-linux64.zip

# Further steps...
echo "Environment setup complete."
