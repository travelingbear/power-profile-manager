#!/bin/bash
set -e

echo "Installing Power Profile Manager GUI components..."

# Install GUI
sudo mkdir -p /usr/local/share/power-profile-manager
sudo cp power-profile-config.py /usr/local/share/power-profile-manager/
sudo chmod +x /usr/local/share/power-profile-manager/power-profile-config.py

# Install desktop entry
sudo cp power-profile-config.desktop /usr/share/applications/
sudo update-desktop-database 2>/dev/null || true

# Install Argos script
mkdir -p ~/.config/argos
cp ../argos/power-profile.30s.sh ~/.config/argos/
chmod +x ~/.config/argos/power-profile.30s.sh

echo ""
echo "GUI components installed!"
echo ""
echo "Argos panel indicator: Restart GNOME Shell (Alt+F2, type 'r', Enter)"
echo "GUI configuration: Search for 'Power Profile Manager' in applications"
echo "Or run: python3 /usr/local/share/power-profile-manager/power-profile-config.py"
