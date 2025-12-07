# Future Development Plans

## Phase 2: GNOME Integration with Argos

### Overview
Argos is a GNOME Shell extension that displays script output in the top panel. We'll create a script that shows current power profile and allows manual control.

### Argos Script Features
- Display current profile icon in top panel
- Shows what mode is being used with a meaningful icon. When hovering mouse over it, it shows what mode is in use.
- Click menu with:
  - Current profile status
  - Battery level and charging state
  - Manual profile override options
  - "Auto" mode (default behavior)

### Implementation
```bash
# ~/.config/argos/power-profile.30s.sh
# Runs every 30 seconds, displays in top panel
```

### Icon States
- ⚡ Performance (AC)
- 🔋 Balanced (Battery >30%)
- 🪫 Power Saving (Battery ≤30%)

### Manual Override
- User can force a profile regardless of battery/AC state
- Override persists until changed or system reboot
- Useful for specific workloads (gaming, compilation, etc.)

## Phase 3: Native C Implementation

### Why C?
- Lower resource usage (no shell spawning)
- Faster execution
- Better integration with system APIs
- Professional daemon implementation
- D-Bus integration for desktop notifications

### Architecture

#### Core Daemon (`power-profiled`)
- Monitors battery via inotify on sysfs
- Event-driven (no polling)
- Applies profiles based on rules
- Exposes D-Bus interface

#### D-Bus Interface
```
org.freedesktop.PowerProfile
  Methods:
    - GetCurrentProfile() -> string
    - SetProfile(string) -> void
    - GetBatteryLevel() -> uint8
  Signals:
    - ProfileChanged(string profile)
```

#### CLI Tool (`power-profile-ctl`)
- Query current profile
- Set manual override
- Show battery status
- Configure thresholds

### Dependencies
- libudev (battery monitoring)
- libdbus (IPC)
- libsystemd (daemon integration)

### File Structure
```
src/
├── daemon.c          # Main daemon
├── battery.c         # Battery monitoring
├── profile.c         # Profile management
├── sysfs.c          # Kernel interface
├── dbus.c           # D-Bus interface
└── config.c         # Configuration parser

include/
└── power-profile.h  # Public API

config/
└── power-profile.conf  # User configuration
```

### Configuration File
```ini
[Thresholds]
PowerSaveThreshold=30
BalancedThreshold=31

[Profiles]
Performance=balance_performance,1,performance
Balanced=balance_power,1,balanced
PowerSave=power,0,low-power

[Behavior]
AutoSwitch=true
NotifyOnChange=true
```

### Build System
- Meson + Ninja (modern, fast)
- pkg-config for dependencies
- systemd integration

### Testing Strategy
1. Unit tests for each module
2. Integration tests with mock sysfs
3. Battery simulation tests
4. Profile switching stress tests
5. Memory leak detection (valgrind)

## Phase 4: Advanced Features

### Adaptive Thresholds
- Learn user patterns
- Adjust thresholds based on usage
- Time-of-day profiles

### Application-Specific Profiles
- Detect running applications
- Apply custom profiles (e.g., IDE = balanced, video = performance)
- Integration with process monitoring

### Power Consumption Tracking
- Log power usage per profile
- Generate reports
- Estimate battery life

### GNOME Settings Integration
- Native settings panel
- Replace Argos with proper extension
- System tray integration
