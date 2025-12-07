# Power Profile Manager - Quick Reference

## Commands

```bash
# Status
power-profile-ctl status

# Live monitoring
power-profile-ctl monitor

# Show configuration
power-profile-ctl config

# Service management
sudo systemctl status power-profiled
sudo systemctl restart power-profiled
sudo systemctl stop power-profiled
sudo systemctl start power-profiled

# View logs
journalctl -u power-profiled -f
journalctl -u power-profiled --since today

# Edit configuration
sudo nano /etc/power-profiled.conf
# Then restart: sudo systemctl restart power-profiled

# Launch GUI
python3 /usr/local/share/power-profile-manager/power-profile-config.py
```

## Configuration File

Location: `/etc/power-profiled.conf`

```ini
THRESHOLD=30    # Battery % to trigger powersave (5-99)
INTERVAL=60     # Check interval in seconds (1-600)
```

## Power Profiles

| Icon | Profile | When | CPU | Turbo | Platform |
|------|---------|------|-----|-------|----------|
| ⚡ | Performance | AC | balance_performance | On | performance |
| 🔋 | Balanced | Battery >30% | balance_power | On | balanced |
| 🪫 | Power Save | Battery ≤30% | power | Off | low-power |

## Files

```
Daemon:       /usr/local/bin/power-profiled
CLI Tool:     /usr/local/bin/power-profile-ctl
Config:       /etc/power-profiled.conf
Service:      /etc/systemd/system/power-profiled.service
State:        /var/run/power-profile-state
GUI:          /usr/local/share/power-profile-manager/power-profile-config.py
Argos:        ~/.config/argos/power-profile.30s.sh
```

## Troubleshooting

```bash
# Check daemon status
systemctl status power-profiled

# Check if running
ps aux | grep power-profiled

# View recent logs
journalctl -u power-profiled --since "10 minutes ago"

# Check battery
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/status

# Check CPU settings
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
cat /sys/devices/system/cpu/intel_pstate/no_turbo
cat /sys/firmware/acpi/platform_profile

# Check TLP
sudo tlp-stat -s

# Restart everything
sudo systemctl restart tlp
sudo systemctl restart power-profiled
```

## Manual Testing

```bash
# Test powersave activation
sudo nano /etc/power-profiled.conf
# Set THRESHOLD to current battery % + 5
sudo systemctl restart power-profiled
power-profile-ctl status  # Should show powersave

# Test AC switching
power-profile-ctl monitor
# Plug/unplug AC and watch changes

# Monitor CPU in real-time
watch -n1 'cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference; \
           cat /sys/devices/system/cpu/intel_pstate/no_turbo; \
           cat /sys/firmware/acpi/platform_profile'
```

## GUI Access

**From Panel:**
- Click battery icon in top panel
- Select "Configure"

**From Applications:**
- Search "Power Profile Manager"

**From Terminal:**
```bash
python3 /usr/local/share/power-profile-manager/power-profile-config.py
```

## Man Pages

```bash
man power-profiled      # Daemon documentation
man power-profile-ctl   # Control tool documentation
```

## Resource Usage

- Memory: ~176KB
- CPU: Near-zero (checks every 60s)
- Startup time: Instant
- Log size: Minimal

## Common Tasks

**Change threshold to 20%:**
```bash
sudo nano /etc/power-profiled.conf
# Change THRESHOLD=30 to THRESHOLD=20
sudo systemctl restart power-profiled
```

**Check every 30 seconds instead of 60:**
```bash
sudo nano /etc/power-profiled.conf
# Change INTERVAL=60 to INTERVAL=30
sudo systemctl restart power-profiled
```

**Disable temporarily:**
```bash
sudo systemctl stop power-profiled
# TLP will continue managing AC/battery normally
```

**Re-enable:**
```bash
sudo systemctl start power-profiled
```

## Version

Current: 1.0.0

Check: `cat ~/Documents/PROJECTS/power-profile-manager/VERSION`
