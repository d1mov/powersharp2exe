#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "[*] Checking if python3 is installed"
if ! command_exists python3; then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt-get update
    sudo apt-get install -y python3
else
    echo "Python3 is already installed."
fi

echo "[*] Checking if pip is installed"
if ! command_exists pip3; then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt-get install -y python3-pip
else
    echo "pip3 is already installed."
fi

echo "[*] Checking if PyQt6 is installed"
if ! python3 -c "import PyQt6" >/dev/null 2>&1; then
    echo "PyQt6 is not installed. Installing PyQt6..."
    sudo pip3 install PyQt6
else
    echo "PyQt6 is already installed."
fi

echo "[*] Checking if csc compiler is installed"
if ! command_exists csc; then
    echo "csc compiler is not installed. Installing Mono..."
    sudo apt-get install -y mono-complete
else
    echo "csc compiler is already installed."
fi

echo "[*] Installing...Please wait..."
PROGRAM_DIR="/usr/share/powersharp2exe"
sudo mkdir -p $PROGRAM_DIR
sudo cp -r ./* $PROGRAM_DIR
sudo chmod +x $PROGRAM_DIR/powersharp2exe.py
sudo rm $PROGRAM_DIR/install.sh

DESKTOP_ENTRY="[Desktop Entry]
Type=Application
Name=powersharp2exe
Exec=/usr/bin/powersharp2exe
Path=/usr/share/powersharp2exe
Icon=$PROGRAM_DIR/img/powersharp2exe.png
Categories=Utility;"

echo "$DESKTOP_ENTRY" > /usr/share/applications/powersharp2exe.desktop

sudo ln -sf /usr/share/powersharp2exe/powersharp2exe.py /usr/bin/powersharp2exe
sudo chmod +x /usr/bin/powersharp2exe

echo "[*] Installation complete."
echo "# You can now run the tool using 'powersharp2exe' in the terminal or access it from applications panel"
echo "# Coded by v1k (Radostin Dimov)"
