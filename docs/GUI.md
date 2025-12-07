# Power Profile Manager - GUI Components

## Argos Panel Indicator

A GNOME Shell top panel indicator that shows current power profile status.

### Features

**Panel Display:**
- ⚡ Performance mode (on AC)
- 🔋 Balanced mode (battery >30%)
- 🪫 Power Save mode (battery ≤30%)
- Battery percentage

**Dropdown Menu:**
- Current battery level and status
- Active profile
- CPU settings (EPP, Turbo, Platform)
- Quick actions:
  - Configure (opens GUI)
  - Monitor (live monitoring)
  - Restart Daemon
  - View Logs
  - About

### Installation

```bash
cd ~/Documents/PROJECTS/power-profile-manager/gui
./install-gui.sh
```

After installation, restart GNOME Shell:
- Press `Alt+F2`
- Type `r`
- Press `Enter`

The indicator will appear in your top panel.

### Location

Script: `~/.config/argos/power-profile.30s.sh`

Refresh interval: 30 seconds (change filename to adjust, e.g., `power-profile.60s.sh` for 60 seconds)

## GTK Configuration GUI

A graphical interface to configure power profile settings.

### Features

- View current battery status and active profile
- Adjust battery threshold (1-99%)
- Adjust check interval (10-600 seconds)
- Save and automatically restart daemon
- User-friendly with validation

### Usage

**From Applications Menu:**
Search for "Power Profile Manager"

**From Command Line:**
```bash
python3 /usr/local/share/power-profile-manager/power-profile-config.py
```

**From Argos Menu:**
Click panel indicator → Configure

### Settings

**Battery Threshold:**
- Range: 1-99%
- Default: 30%
- When battery drops to or below this level, ultra power-saving mode activates

**Check Interval:**
- Range: 10-600 seconds
- Default: 60 seconds
- How often the daemon checks battery status

### Technical Details

- Built with GTK 3
- Uses `pkexec` for privilege elevation
- Automatically restarts daemon after saving
- Validates input ranges
- Shows success/error dialogs

## Files

```
gui/
├── power-profile-config.py          # GTK GUI application
├── power-profile-config.desktop     # Desktop entry
└── install-gui.sh                   # Installation script

argos/
└── power-profile.30s.sh            # Argos panel indicator

Installed locations:
├── /usr/local/share/power-profile-manager/power-profile-config.py
├── /usr/share/applications/power-profile-config.desktop
└── ~/.config/argos/power-profile.30s.sh
```

## Requirements

- GNOME Shell with Argos extension
- Python 3 with GTK 3 bindings (python3-gi)
- pkexec (polkit)
- zenity (for dialogs)

## Troubleshooting

**Argos indicator not showing:**
- Ensure Argos extension is enabled
- Restart GNOME Shell (Alt+F2, type 'r')
- Check script is executable: `chmod +x ~/.config/argos/power-profile.30s.sh`

**GUI won't launch:**
- Check GTK is installed: `python3 -c "import gi; gi.require_version('Gtk', '3.0')"`
- Install if missing: `sudo apt install python3-gi`

**Can't save configuration:**
- Ensure pkexec is installed: `which pkexec`
- Check daemon is running: `systemctl status power-profiled`

## Screenshots

### Panel Indicator
```
🔋 52%  ← Click to open menu
```

### Dropdown Menu
```
Power Profile Manager
---
Battery: 52% (Discharging)
Active Profile: Balanced
---
CPU Settings:
  EPP: balance_power
  Turbo: Enabled
  Platform: balanced
---
🔧 Configure
📊 Monitor
🔄 Restart Daemon
---
📖 View Logs
ℹ️ About
```

### Configuration GUI
```
┌─────────────────────────────────────────┐
│  Power Profile Manager                  │
│                                         │
│  Battery: 52%                           │
│  Power Status: Discharging              │
│  Active Profile: Balanced               │
│  ─────────────────────────────────────  │
│  Configuration                          │
│                                         │
│  Battery Threshold (%): [30]            │
│  Trigger ultra power-saving at this...  │
│                                         │
│  Check Interval (seconds): [60]         │
│  How often to check battery status      │
│  ─────────────────────────────────────  │
│                    [Save & Restart] [Cancel] │
└─────────────────────────────────────────┘
```
