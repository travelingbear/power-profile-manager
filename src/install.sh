#!/bin/bash
set -e

echo "Building power-profiled and power-profile-ctl..."
make clean
make

echo "Installing daemon and control tool..."
sudo make install

echo "Installing configuration file..."
if [ ! -f /etc/power-profiled.conf ]; then
    sudo cp power-profiled.conf /etc/
    echo "Configuration installed to /etc/power-profiled.conf"
else
    echo "Configuration file already exists, skipping"
fi

echo "Installing man pages..."
sudo mkdir -p /usr/local/share/man/man1 /usr/local/share/man/man8
sudo cp ../docs/power-profile-ctl.1 /usr/local/share/man/man1/
sudo cp ../docs/power-profiled.8 /usr/local/share/man/man8/
sudo mandb -q 2>/dev/null || true

echo "Installing systemd service..."
sudo cp power-profiled.service /etc/systemd/system/

echo "Reloading systemd..."
sudo systemctl daemon-reload

echo "Enabling and starting service..."
sudo systemctl enable power-profiled.service
sudo systemctl start power-profiled.service

echo ""
echo "Installation complete!"
echo ""
echo "Commands:"
echo "  power-profile-ctl status   - Show current status"
echo "  power-profile-ctl monitor  - Live monitoring"
echo "  power-profile-ctl config   - Show configuration"
echo ""
echo "Service management:"
echo "  systemctl status power-profiled"
echo "  journalctl -u power-profiled -f"
echo ""
echo "Documentation:"
echo "  man power-profiled"
echo "  man power-profile-ctl"
