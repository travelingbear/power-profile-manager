# Power Profile Manager - Installation Guide

Complete installation guide for Power Profile Manager v1.0.0

## Prerequisites

### Required
- Linux with systemd
- TLP power management tool
- GCC compiler
- Root/sudo access

### Optional (for GUI)
- GNOME Shell with Argos extension
- Python 3 with GTK 3 bindings (python3-gi)
- pkexec (polkit)
- zenity

## Quick Install (All Components)

```bash
# 1. Install TLP
sudo apt install tlp tlp-rdw  # Debian/Ubuntu
# OR
sudo dnf install tlp tlp-rdw  # Fedora
# OR
sudo pacman -S tlp            # Arch

# 2. Configure TLP
sudo nano /etc/tlp.d/01-power-profile.conf
# Copy configuration from README.md

sudo tlp start

# 3. Install daemon and CLI tools
cd ~/Documents/PROJECTS/power-profile-manager/src
./install.sh

# 4. Install GUI components (optional)
cd ~/Documents/PROJECTS/power-profile-manager/gui
./install-gui.sh

# 5. Restart GNOME Shell (for Argos)
# Press Alt+F2, type 'r', Enter
```

## Step-by-Step Installation

### 1. Install TLP

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install tlp tlp-rdw
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

**Fedora:**
```bash
sudo dnf install tlp tlp-rdw
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

**Arch Linux:**
```bash
sudo pacman -S tlp
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

### 2. Configure TLP

Create `/etc/tlp.d/01-power-profile.conf`:

```ini
# CPU Performance - High on AC, Balanced on Battery
CPU_ENERGY_PERF_POLICY_ON_AC=balance_performance
CPU_ENERGY_PERF_POLICY_ON_BAT=balance_power

# CPU Boost - Enable on both AC and Battery
CPU_BOOST_ON_AC=1
CPU_BOOST_ON_BAT=1

# Platform Profile - Performance on AC, Balanced on Battery
PLATFORM_PROFILE_ON_AC=performance
PLATFORM_PROFILE_ON_BAT=balanced

# Disk Power Management
DISK_APM_LEVEL_ON_AC="254 254"
DISK_APM_LEVEL_ON_BAT="128 128"

# SATA Link Power Management
SATA_LINKPWR_ON_AC="med_power_with_dipm"
SATA_LINKPWR_ON_BAT="med_power_with_dipm"

# Runtime Power Management
AHCI_RUNTIME_PM_ON_AC=on
AHCI_RUNTIME_PM_ON_BAT=auto
RUNTIME_PM_ON_AC=on
RUNTIME_PM_ON_BAT=auto

# WiFi Power Saving
WIFI_PWR_ON_AC=off
WIFI_PWR_ON_BAT=on

# Battery Care (optional)
START_CHARGE_THRESH_BAT0=75
STOP_CHARGE_THRESH_BAT0=80

# USB Autosuspend
USB_AUTOSUSPEND=1
```

Apply configuration:
```bash
sudo tlp start
```

### 3. Install Power Profile Manager Daemon

```bash
cd ~/Documents/PROJECTS/power-profile-manager/src
chmod +x install.sh
./install.sh
```

This installs:
- `/usr/local/bin/power-profiled` - Main daemon
- `/usr/local/bin/power-profile-ctl` - Control tool
- `/etc/power-profiled.conf` - Configuration file
- `/etc/systemd/system/power-profiled.service` - Systemd service
- `/usr/local/share/man/man8/power-profiled.8` - Man page (daemon)
- `/usr/local/share/man/man1/power-profile-ctl.1` - Man page (control tool)

Verify installation:
```bash
systemctl status power-profiled
power-profile-ctl status
```

### 4. Install GUI Components (Optional)

**Prerequisites:**

1. **Install Argos GNOME Extension:**
   
   Visit https://extensions.gnome.org/extension/1176/argos/ and click "Install"
   
   OR install via command line:
   ```bash
   # Download and install
   cd /tmp
   wget https://extensions.gnome.org/extension-data/argospew.worldwidemann.com.v3.shell-extension.zip
   gnome-extensions install argospew.worldwidemann.com.v3.shell-extension.zip
   gnome-extensions enable argos@pew.worldwidemann.com
   ```
   
   Verify installation:
   ```bash
   gnome-extensions list | grep argos
   ```

2. **Install Python GTK bindings:**
   ```bash
   # Debian/Ubuntu
   sudo apt install python3-gi zenity
   
   # Fedora
   sudo dnf install python3-gobject zenity
   
   # Arch
   sudo pacman -S python-gobject zenity
   ```

**Install GUI:**
```bash
cd ~/Documents/PROJECTS/power-profile-manager/gui
chmod +x install-gui.sh
./install-gui.sh
```

This installs:
- `/usr/local/share/power-profile-manager/power-profile-config.py` - GTK GUI
- `/usr/share/applications/power-profile-config.desktop` - Desktop entry
- `~/.config/argos/power-profile.10s.sh` - Argos panel indicator

**Activate Argos indicator:**
- Press `Alt+F2`
- Type `r` and press `Enter` (restarts GNOME Shell)
- Look for battery icon (⚡/🔋/🪫) in top panel

**Change Argos refresh rate:**
```bash
# For 5-second refresh
mv ~/.config/argos/power-profile.10s.sh ~/.config/argos/power-profile.5s.sh

# For 30-second refresh
mv ~/.config/argos/power-profile.10s.sh ~/.config/argos/power-profile.30s.sh
```

## Configuration

### Daemon Configuration

Edit `/etc/power-profiled.conf`:

```ini
# Battery threshold (5-99%)
THRESHOLD=30

# Check interval (1-600 seconds)
INTERVAL=60
```

Restart daemon after changes:
```bash
sudo systemctl restart power-profiled
```

Valid ranges:
- THRESHOLD: 5-99 (percentage)
- INTERVAL: 1-600 (seconds)

**Note:** Very low intervals (1-5 seconds) will check more frequently but still have negligible CPU impact.

### Using GUI

1. Click Argos panel indicator → Configure
2. OR search "Power Profile Manager" in applications
3. Adjust settings
4. Click "Save & Restart"

## Verification

### Check Daemon Status
```bash
systemctl status power-profiled
journalctl -u power-profiled -f
```

### Check Current Profile
```bash
power-profile-ctl status
```

### Live Monitoring
```bash
power-profile-ctl monitor
```

### Test Profile Switching

1. **Test powersave mode:**
   ```bash
   # Temporarily set threshold to current battery level
   sudo nano /etc/power-profiled.conf
   # Set THRESHOLD to current battery % or higher
   sudo systemctl restart power-profiled
   power-profile-ctl status  # Should show "powersave"
   ```

2. **Test AC switching:**
   - Plug/unplug AC adapter
   - Watch `power-profile-ctl monitor`
   - TLP should handle transitions instantly

## Troubleshooting

### Daemon not starting
```bash
sudo systemctl status power-profiled
journalctl -u power-profiled --since today
```

### TLP conflicts
```bash
sudo tlp-stat -s
# Ensure TLP is running and configured correctly
```

### GUI not launching
```bash
# Check GTK installation
python3 -c "import gi; gi.require_version('Gtk', '3.0')"

# Install if missing
sudo apt install python3-gi  # Debian/Ubuntu
sudo dnf install python3-gobject  # Fedora
```

### Argos indicator not showing
```bash
# Check Argos extension is enabled
gnome-extensions list | grep argos

# Check script exists and is executable
ls -l ~/.config/argos/power-profile.30s.sh
chmod +x ~/.config/argos/power-profile.30s.sh

# Restart GNOME Shell
# Alt+F2, type 'r', Enter
```

## Uninstallation

### Remove Daemon
```bash
sudo systemctl stop power-profiled
sudo systemctl disable power-profiled
sudo rm /usr/local/bin/power-profiled
sudo rm /usr/local/bin/power-profile-ctl
sudo rm /etc/systemd/system/power-profiled.service
sudo rm /etc/power-profiled.conf
sudo rm /usr/local/share/man/man1/power-profile-ctl.1
sudo rm /usr/local/share/man/man8/power-profiled.8
sudo systemctl daemon-reload
sudo mandb -q
```

### Remove GUI
```bash
sudo rm /usr/local/share/power-profile-manager/power-profile-config.py
sudo rmdir /usr/local/share/power-profile-manager
sudo rm /usr/share/applications/power-profile-config.desktop
rm ~/.config/argos/power-profile.30s.sh
sudo update-desktop-database
```

### Keep TLP
TLP can remain installed and will continue managing AC/battery transitions normally.

## Next Steps

- Read `man power-profiled` for detailed daemon documentation
- Read `man power-profile-ctl` for control tool usage
- See `docs/GUI.md` for GUI documentation
- Check `CHANGELOG.md` for version history
- Review `docs/FUTURE_PLANS.md` for upcoming features

## Support

- Documentation: `~/Documents/PROJECTS/power-profile-manager/docs/`
- Man pages: `man power-profiled`, `man power-profile-ctl`
- Logs: `journalctl -u power-profiled -f`
