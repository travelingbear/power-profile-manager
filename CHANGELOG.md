# Changelog

All notable changes to Power Profile Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-07

### Added
- **Travel Mode**: New feature to temporarily increase battery charge threshold to 95%
- Visual indicator: Backpack icon (🎒) in panel when Travel Mode is enabled
- One-click toggle in Argos menu: "Enable/Disable Travel Mode"
- Travel mode status display in menu: "Travel Mode: ON/OFF (charging to 95%/90%)"
- Persistent travel mode state (survives reboots until manually disabled)
- Comprehensive travel mode documentation (TRAVEL_MODE.md)

### Changed
- Panel icon now shows backpack (🎒) when in Travel Mode, overriding normal battery/plug icons
- Battery charge thresholds updated: Normal mode 75-90%, Travel mode 75-95%
- Argos menu now displays current travel mode status
- Profile display shows "(Travel Mode)" suffix when active

### Technical Details
- Travel mode state stored in `~/.config/power-profile-manager/travel-mode`
- Instant threshold changes via `tlp setcharge` command
- No restart required - changes apply immediately
- TLP config automatically updated when toggling modes
- 15% hysteresis gap (normal) or 20% gap (travel) reduces charge cycles

## [1.0.3] - 2025-12-07

### Fixed
- Fixed AC detection when battery reaches charge threshold and stops charging
- Daemon now uses hybrid AC detection: checks `/sys/class/power_supply/AC/online` first, falls back to battery status
- Correctly handles "Not charging" battery status when at TLP charge threshold (e.g., 75-80%)
- Performance mode now maintained when AC connected, regardless of battery charging state

### Changed
- Improved `is_on_ac()` function to prioritize AC adapter status over battery status
- Added "Not charging" to recognized AC-connected battery states
- More reliable AC detection for systems with battery charge thresholds configured

### Added
- Comprehensive test suite (TEST_RESULTS.md) validating all power modes and transitions
- Argos panel indicator now uses AC adapter status for icon selection
- Updated Argos script to show plug icon (🔌) when AC connected, battery icons when on battery

### Technical Details
- Hybrid AC detection prevents false battery mode when AC is connected but battery not charging
- All three power modes validated through extensive testing:
  * Performance (AC) - working correctly
  * Balanced (battery >threshold) - working correctly  
  * Ultra Power Save (battery ≤threshold) - working correctly
- Daemon survives sleep/wake cycles and auto-starts on boot (16s delay)
- Mode transitions occur within 5-second check interval

## [1.0.2] - 2025-12-07

### Fixed
- Fixed critical bug where daemon continued enforcing powersave mode when AC was connected
- Fixed daemon not triggering TLP mode transitions when switching between AC and battery
- Daemon now properly detects AC/battery state changes and triggers appropriate TLP modes

### Changed
- Daemon now actively triggers `tlp ac` when AC is connected (ensures Performance mode)
- Daemon now actively triggers `tlp bat` when on battery above threshold (ensures Balanced mode)
- Added state transition tracking to detect AC plug/unplug events
- Improved mode switching logic for seamless transitions between all three power modes

### Technical Details
- All three power modes now work correctly:
  - Performance (balance_performance) when AC connected - managed by TLP
  - Balanced (balance_power) when battery >threshold - managed by TLP
  - Ultra Power Save (power) when battery ≤threshold - enforced by daemon
- Daemon backs off completely when not in Ultra Power Save mode
- TLP transitions are triggered immediately upon state changes

## [1.0.1] - 2025-12-07

### Fixed
- Fixed circular dependency in systemd service that prevented auto-start on boot
- Changed service dependency from `After=tlp.service` to `After=multi-user.target tlp.service`
- Added `Requires=tlp.service` to ensure TLP is running before daemon starts
- Added runtime check in daemon to verify TLP service is active

### Added
- Daemon status indicator in Argos menu (shows if daemon is running)
- TLP status indicator in Argos menu (shows if TLP is running)
- Click-to-start functionality for stopped services in Argos menu
- Daemon status display in GTK configuration GUI
- Hide Battery Indicator GNOME extension (minimal extension to hide native battery icon)

### Changed
- Argos menu now shows plain text status (removed colors and icons from service status)
- Improved error messages when TLP is not running
- Enhanced logging with TLP integration note

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
