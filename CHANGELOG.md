# Changelog

All notable changes to Power Profile Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-07

### Added
- Native C daemon for power profile management
- Three-tier power management: Performance (AC), Balanced (Battery >threshold%), Ultra Power Save (Battery ≤threshold%)
- Configuration file support (`/etc/power-profiled.conf`)
- Configurable battery threshold (5-99%)
- Configurable check interval (1-600 seconds)
- CLI control tool (`power-profile-ctl`) with commands:
  - `status` - Show current power profile status
  - `monitor` - Live monitoring of power profile (2s refresh)
  - `config` - Show current configuration
  - `help` - Command help
- **Argos GNOME Shell panel indicator**
  - Real-time battery and profile display with icons (⚡🔋🪫)
  - Dropdown menu with CPU settings
  - Quick actions (configure, monitor, restart, logs, about)
  - 10-second refresh rate (configurable via filename)
- **GTK configuration GUI**
  - Graphical interface to edit settings
  - Real-time status display
  - Automatic daemon restart after save
  - Single password prompt (combined pkexec operations)
  - Input validation with proper ranges
- Systemd service integration
- Efficient hybrid design with TLP
- Syslog logging with proper error handling
- Comprehensive documentation (README, INSTALL, man pages, GUI docs)
- Intel and AMD CPU support
- Proper C implementation (no shell spawning, uses glob() for file iteration)

### Technical Details
- Memory footprint: ~176KB
- CPU usage: Near-zero (configurable check interval)
- Event-driven profile switching
- No conflicts with TLP
- Whitespace-tolerant config parsing
- Graceful error handling and logging

### Design Philosophy
- TLP handles AC/battery transitions (instant response)
- Daemon only intervenes at critical battery levels (≤threshold)
- Minimal overhead and resource usage
- Clean separation of concerns
- User-friendly with multiple interfaces (CLI, GUI, panel indicator)

### Files Installed
- `/usr/local/bin/power-profiled` - Main daemon
- `/usr/local/bin/power-profile-ctl` - Control tool
- `/etc/power-profiled.conf` - Configuration file
- `/etc/systemd/system/power-profiled.service` - Systemd service
- `/usr/local/share/man/man8/power-profiled.8` - Daemon man page
- `/usr/local/share/man/man1/power-profile-ctl.1` - Control tool man page
- `/usr/local/share/power-profile-manager/power-profile-config.py` - GTK GUI
- `/usr/share/applications/power-profile-config.desktop` - Desktop entry
- `~/.config/argos/power-profile.10s.sh` - Argos panel indicator

[1.0.0]: https://github.com/yourusername/power-profile-manager/releases/tag/v1.0.0

### Technical Details
- Memory footprint: ~176KB
- CPU usage: Minimal (checks every 60s by default)
- Event-driven profile switching
- No conflicts with TLP

### Design Philosophy
- TLP handles AC/battery transitions (instant response)
- Daemon only intervenes at critical battery levels (≤threshold)
- Minimal overhead and resource usage
- Clean separation of concerns

[1.0.0]: https://github.com/yourusername/power-profile-manager/releases/tag/v1.0.0
