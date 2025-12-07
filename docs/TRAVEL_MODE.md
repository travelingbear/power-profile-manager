# Travel Mode

## Overview

Travel Mode allows you to temporarily increase the battery charge threshold from 90% to 95%, giving you extra capacity when you need maximum runtime away from AC power.

## Visual Indicator

When Travel Mode is enabled, the Argos panel indicator changes from the normal battery/plug icons to a backpack icon (🎒), providing a constant visual reminder that the mode is active.

**Normal Mode:**
- 🔌 (AC connected)
- 🔋 (Battery, above threshold)
- 🪫 (Battery, below threshold)

**Travel Mode:**
- 🎒 (Always shows backpack, regardless of AC/battery status)

## How to Use

### Enable Travel Mode

1. Click the Power Profile Manager icon in the panel
2. Click "Enable Travel Mode"
3. The panel icon changes to 🎒
4. Battery will charge to 95% (instead of 90%)

### Disable Travel Mode

1. Click the backpack icon (🎒) in the panel
2. Click "Disable Travel Mode"
3. The panel icon returns to normal (🔌/🔋/🪫)
4. Battery will charge to 90% on next charge cycle

## Battery Thresholds

| Mode | Start Charging | Stop Charging | Hysteresis Gap |
|------|----------------|---------------|----------------|
| Normal | 75% | 90% | 15% |
| Travel | 75% | 95% | 20% |

## When to Use Travel Mode

**Enable Travel Mode when:**
- Going on a trip where AC access is limited
- Need maximum battery capacity for extended work sessions
- Traveling and want extra runtime buffer

**Disable Travel Mode when:**
- Back at your desk with regular AC access
- Want to maximize battery longevity
- Don't need the extra 5% capacity

## Battery Health Considerations

- **90% threshold**: Optimal for daily use, excellent battery longevity
- **95% threshold**: Still safe, minimal additional stress
- **Recommendation**: Only use Travel Mode when you actually need the extra capacity

## Technical Details

### What Happens When You Toggle

**Enable:**
1. Creates flag file: `~/.config/power-profile-manager/travel-mode`
2. Updates TLP config: `STOP_CHARGE_THRESH_BAT0=95`
3. Applies immediately: `tlp setcharge 75 95 BAT0`
4. Battery starts charging to 95% (if on AC and below 95%)

**Disable:**
1. Removes flag file
2. Updates TLP config: `STOP_CHARGE_THRESH_BAT0=90`
3. Applies immediately: `tlp setcharge 75 90 BAT0`
4. Battery stops at 90% on next charge cycle

### No Restart Required

Changes take effect immediately - no need to restart the laptop, daemon, or any services.

## Menu Display

The Argos menu shows the current travel mode status:

```
Power Profile Manager
---
Daemon: Running
TLP: Running
---
Battery: 77% (Not charging)
Active Profile: Performance (Travel Mode)
Travel Mode: ON (charging to 95%)
---
```

## Icon Priority

Travel Mode icon (🎒) takes priority over all other icons:
- Overrides AC/battery status icons
- Provides constant visual reminder
- AC/battery status still visible in menu

## Tips

1. **Visual Reminder**: The backpack icon ensures you won't forget to disable Travel Mode when you're back
2. **One-Click Toggle**: Easy to enable before travel, disable when back
3. **Instant Effect**: Battery starts charging to 95% immediately when enabled
4. **Persistent**: Setting survives reboots until manually disabled
