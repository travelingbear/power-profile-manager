# Power Profile Manager

Dynamic power management system for Linux laptops with battery percentage-based profiles.

**Version:** 1.0.0

## Features

- Native C daemon for optimal performance (~176KB memory)
- Three power profiles: Performance, Balanced, Ultra Power Saving
- Automatic switching based on AC/battery and battery percentage
- Configurable battery threshold and check interval
- CLI monitoring and control tool (`power-profile-ctl`)
- Efficient design: TLP handles AC/battery transitions, daemon only intervenes at critical battery levels
- Systemd service integration
- Comprehensive documentation (man pages)

## Quick Start

```bash
# Check current status
power-profile-ctl status

# Live monitoring
power-profile-ctl monitor

# View configuration
power-profile-ctl config

# Check service status
systemctl status power-profiled

# View logs
journalctl -u power-profiled -f
```

## Installation

### 1. Install TLP

**Debian/Ubuntu:**
```bash
sudo apt install tlp tlp-rdw
```

**Fedora:**
```bash
sudo dnf install tlp tlp-rdw
```

**Arch:**
```bash
sudo pacman -S tlp
```

Enable TLP:
```bash
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

### 2. Configure TLP

Create or edit `/etc/tlp.d/01-power-profile.conf`:

```bash
sudo nano /etc/tlp.d/01-power-profile.conf
```

Add this configuration:

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

# Battery Care (optional - adjust for your preference)
START_CHARGE_THRESH_BAT0=75
STOP_CHARGE_THRESH_BAT0=80

# USB Autosuspend
USB_AUTOSUSPEND=1
```

Apply TLP configuration:
```bash
sudo tlp start
```

### 3. Install Power Profile Manager

```bash
cd ~/Documents/PROJECTS/power-profile-manager/src
chmod +x install.sh
./install.sh
```

The installer will:
- Build the daemon and control tool
- Install binaries to `/usr/local/bin/`
- Install configuration to `/etc/power-profiled.conf`
- Install man pages
- Set up and start systemd service

### 4. Install GUI Components (Optional)

**Prerequisites:**
1. Install Argos GNOME extension:
   - Visit https://extensions.gnome.org/extension/1176/argos/
   - Click "Install" and enable the extension
   - OR install via command line:
     ```bash
     # For GNOME 40+
     gnome-extensions install argos@pew.worldwidemann.com
     gnome-extensions enable argos@pew.worldwidemann.com
     ```

2. Install Python GTK bindings:
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

**Activate Argos indicator:**
- Press `Alt+F2`
- Type `r` and press `Enter` (restarts GNOME Shell)
- Look for battery icon in top panel

## How It Works

The system uses a two-tier approach for maximum efficiency:

- **On AC**: TLP applies performance settings instantly
- **On Battery >30%**: TLP applies balanced settings (daemon stays inactive)
- **On Battery ≤30%**: Daemon overrides to ultra power-saving mode

**Why this design?**
- TLP handles all AC/battery transitions natively (instant response)
- Daemon only intervenes when battery is critical (≤threshold)
- No conflicts or redundant operations
- Minimal overhead (~176KB memory, checks every 60s)

### Profiles

| Profile | CPU Policy | Turbo | Platform | When | Managed By |
|---------|-----------|-------|----------|------|------------|
| Performance | balance_performance | On | performance | AC Power | TLP |
| Balanced | balance_power | On | balanced | Battery >30% | TLP |
| Ultra Power Save | power | Off | low-power | Battery ≤30% | Daemon |

## Configuration

Edit `/etc/power-profiled.conf`:

```ini
# Battery threshold (percentage) to trigger ultra power-saving mode
# Default: 30
THRESHOLD=30

# Check interval in seconds
# Default: 60
INTERVAL=60
```

After editing, restart the daemon:
```bash
sudo systemctl restart power-profiled
```

Valid ranges:
- THRESHOLD: 5-99 (percentage)
- INTERVAL: 1-600 (seconds)

**Note:** Very low intervals (1-5 seconds) will check more frequently but still have negligible CPU impact (~0.002%).

## Commands

### power-profile-ctl

```bash
# Show current status (default)
power-profile-ctl
power-profile-ctl status

# Live monitoring (updates every 2 seconds)
power-profile-ctl monitor

# Show configuration
power-profile-ctl config

# Show help
power-profile-ctl help
```

### Service Management

```bash
# Check service status
systemctl status power-profiled

# Start/stop service
sudo systemctl start power-profiled
sudo systemctl stop power-profiled

# Enable/disable autostart
sudo systemctl enable power-profiled
sudo systemctl disable power-profiled

# Restart after config changes
sudo systemctl restart power-profiled

# View logs
journalctl -u power-profiled -f
journalctl -u power-profiled --since today
```

## Testing

Monitor CPU settings in real-time:
```bash
watch -n1 'cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference; \
           cat /sys/devices/system/cpu/intel_pstate/no_turbo; \
           cat /sys/firmware/acpi/platform_profile'
```

Check battery:
```bash
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/status
```

Monitor profile changes:
```bash
journalctl -u power-profiled -f
```

## Troubleshooting

**Daemon not running:**
```bash
sudo systemctl status power-profiled
sudo systemctl restart power-profiled
```

**Check if TLP is active:**
```bash
sudo tlp-stat -s
```

**View detailed logs:**
```bash
journalctl -u power-profiled --since today
journalctl -u tlp --since today
```

**Manually test daemon:**
```bash
sudo systemctl stop power-profiled
sudo /usr/local/bin/power-profiled
# Press Ctrl+C to stop
sudo systemctl start power-profiled
```

## Documentation

Man pages are available:
```bash
man power-profiled    # Daemon documentation
man power-profile-ctl # Control tool documentation
```

## Project Structure

```
power-profile-manager/
├── VERSION                  # Version number
├── CHANGELOG.md            # Version history
├── README.md               # This file
├── docs/
│   ├── REQUIREMENTS.md     # Detailed requirements
│   ├── FUTURE_PLANS.md     # Roadmap
│   ├── power-profiled.8    # Man page (daemon)
│   └── power-profile-ctl.1 # Man page (control tool)
├── src/
│   ├── power-profiled.c         # Main daemon
│   ├── power-profile-ctl.c      # Control tool
│   ├── power-profiled.conf      # Configuration template
│   ├── power-profiled.service   # Systemd service
│   ├── Makefile                 # Build system
│   └── install.sh               # Installation script
└── scripts/
    └── (legacy bash implementation)
```

## Roadmap

- [x] Phase 1: Native C daemon (v1.0)
- [ ] Phase 2: GNOME integration via Argos extension (top panel indicator)
- [ ] Phase 3: GUI configuration tool
- [ ] Phase 4: Advanced features (adaptive thresholds, app-specific profiles)

See [FUTURE_PLANS.md](docs/FUTURE_PLANS.md) for detailed roadmap.

## Requirements

- Linux kernel with intel_pstate or amd-pstate
- TLP installed and running
- systemd
- Root access for installation
- GCC for building from source

### Optional (for GUI components)
- GNOME Shell 3.36 or newer
- Argos GNOME extension (https://extensions.gnome.org/extension/1176/argos/)
- Python 3 with GTK 3 bindings (python3-gi)
- pkexec (polkit)
- zenity

## Uninstallation

```bash
# Stop and disable service
sudo systemctl stop power-profiled
sudo systemctl disable power-profiled

# Remove files
sudo rm /usr/local/bin/power-profiled
sudo rm /usr/local/bin/power-profile-ctl
sudo rm /etc/systemd/system/power-profiled.service
sudo rm /etc/power-profiled.conf
sudo rm /usr/local/share/man/man1/power-profile-ctl.1
sudo rm /usr/local/share/man/man8/power-profiled.8

# Reload systemd
sudo systemctl daemon-reload
sudo mandb -q
```

## License

TBD

## Author

Francisco (2025)

## Contributing

See [CHANGELOG.md](CHANGELOG.md) for version history.
