# Power Profile Manager - Requirements

## Problem Statement
TLP provides only two modes (AC/BAT) but doesn't support battery percentage-based profiles. Performance is too low on battery due to aggressive power-saving defaults.

## Goals
Create a dynamic power management system with three profiles:
1. **Performance** - When on AC power
2. **Balanced** - When on battery with >30% charge
3. **Ultra Power Saving** - When battery ≤30%

## Current Implementation (Phase 1)

### Hybrid Approach with TLP
- TLP handles AC/BAT transitions and manages non-CPU settings (disks, USB, WiFi)
- Custom script monitors battery percentage and overrides CPU performance settings
- Script runs periodically (systemd timer) to check and adjust

### Settings per Profile

**Performance (AC - TLP managed)**
- CPU Energy Policy: balance_performance
- CPU Turbo Boost: Enabled
- Platform Profile: performance

**Balanced (Battery >30% - Script managed)**
- CPU Energy Policy: balance_power
- CPU Turbo Boost: Enabled
- Platform Profile: balanced

**Ultra Power Saving (Battery ≤30% - Script managed)**
- CPU Energy Policy: power
- CPU Turbo Boost: Disabled
- Platform Profile: low-power

## Future Plans (Phase 2)

### GNOME Integration via Argos Extension
- Top panel icon showing current profile
- Click to see battery percentage and active profile
- Manual profile override controls
- Visual feedback for profile changes

### Native C Implementation (Phase 3)
- Replace bash script with C daemon for efficiency
- Direct system calls for better performance
- Reduced overhead (no shell spawning)
- Integration with D-Bus for GNOME communication
- Proper signal handling and logging

## Technical Considerations

### Battery Detection
- Primary: `/sys/class/power_supply/BAT0/`
- Fallback: `/sys/class/power_supply/BAT1/` (for some ThinkPads)

### CPU Control Interfaces
- Intel: `/sys/devices/system/cpu/intel_pstate/`
- AMD: `/sys/devices/system/cpu/cpufreq/`
- Platform: `/sys/firmware/acpi/platform_profile`

### State Management
- Track current profile to avoid redundant writes
- Persist state across script invocations
- Log profile changes for debugging

## Testing Requirements
- Test on AC power
- Test battery transitions at various levels
- Test rapid profile switching
- Verify no conflicts with TLP
- Monitor CPU frequency and power consumption
