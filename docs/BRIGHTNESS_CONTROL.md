# Automatic Brightness Control

## Overview

Power Profile Manager can automatically adjust screen brightness based on the active power mode, helping to extend battery life without manual intervention.

## How It Works

### Smart Brightness Logic

The daemon uses intelligent brightness control:
- **Only reduces brightness** - Never increases it
- **Respects manual adjustments** - If you dim the screen, it stays dimmed
- **One-time adjustment** - Sets brightness once when entering a new mode
- **Power-saving focused** - Designed to save battery, not annoy you

### Brightness Levels

Three configurable brightness levels for each power mode:

| Power Mode | Default Brightness | When Active |
|------------|-------------------|-------------|
| Performance | 100% | AC connected |
| Balanced | 80% | Battery > threshold |
| Power Save | 60% | Battery ≤ threshold |

## Configuration

### Enable/Disable

Edit `/etc/power-profiled.conf`:

```bash
# Enable automatic brightness
AUTO_BRIGHTNESS=1

# Disable automatic brightness
AUTO_BRIGHTNESS=0
```

### Customize Brightness Levels

```bash
# Power Save mode (battery ≤ threshold)
BRIGHTNESS_POWERSAVE=60

# Balanced mode (battery > threshold, on battery)
BRIGHTNESS_BALANCED=80

# Performance mode (AC connected)
BRIGHTNESS_PERFORMANCE=100
```

Valid range: 10-100%

### Using the GUI

1. Open Configuration GUI from Argos menu
2. Check "Enable automatic brightness adjustment"
3. Adjust the three brightness sliders
4. Click "Save & Restart"

## Behavior Examples

### Example 1: Manual Dimming Respected

```
Current brightness: 50%
Mode changes to Balanced (80% configured)
Result: Brightness stays at 50% (your preference respected)
```

### Example 2: Automatic Reduction

```
Current brightness: 90%
Mode changes to Power Save (60% configured)
Result: Brightness reduced to 60% (saves power)
```

### Example 3: No Increase on AC

```
Current brightness: 70%
AC plugged in, Performance mode (100% configured)
Result: Brightness stays at 70% (no unwanted increase)
```

## Technical Details

### Brightness Control Path

- Intel backlight: `/sys/class/backlight/intel_backlight/brightness`
- Maximum brightness: Read from `max_brightness` file
- Current brightness: Read before adjustment

### Mode Tracking

The daemon tracks the current mode to avoid repeated adjustments:
- Mode 0: Performance (AC)
- Mode 1: Power Save (battery ≤ threshold)
- Mode 2: Balanced (battery > threshold)

### Logging

Brightness changes are logged to syslog:

```bash
# View brightness logs
journalctl -u power-profiled | grep brightness

# Example output
Dec 07 21:00:00 laptop power-profiled[1234]: Reduced brightness to 60% (mode 1)
Dec 07 21:05:00 laptop power-profiled[1234]: Skipping brightness change: current 50 >= target 80
```

## Compatibility

### Supported Hardware

- Intel integrated graphics (intel_backlight)
- Most modern laptops with standard backlight control

### Unsupported Hardware

If brightness control is not available:
- Daemon logs: "Brightness control not available"
- AUTO_BRIGHTNESS automatically disabled
- No errors or warnings

## Tips

1. **Start Conservative**: Begin with default values (60/80/100)
2. **Adjust Gradually**: Fine-tune based on your preferences
3. **Test Each Mode**: Verify brightness in all three power modes
4. **Disable If Needed**: Set AUTO_BRIGHTNESS=0 if you prefer manual control

## Troubleshooting

### Brightness Not Changing

Check daemon logs:
```bash
journalctl -u power-profiled | grep brightness
```

Verify configuration:
```bash
cat /etc/power-profiled.conf | grep BRIGHTNESS
```

### Brightness Increases Unexpectedly

This should not happen with v1.2.0+. If it does:
1. Check daemon version: `systemctl status power-profiled`
2. Verify you're running v1.2.0 or later
3. Check logs for "Skipping brightness change" messages

### Want Manual Control Only

Disable automatic brightness:
```bash
sudo nano /etc/power-profiled.conf
# Set: AUTO_BRIGHTNESS=0
sudo systemctl restart power-profiled
```

## Integration with Other Tools

### GNOME Settings

Automatic brightness in GNOME Settings is independent:
- GNOME: Time-based dimming
- Power Profile Manager: Mode-based dimming
- Both can coexist

### TLP

TLP does not control screen brightness, so there are no conflicts.

## Performance Impact

- **Memory**: Negligible (< 1KB additional)
- **CPU**: Minimal (one brightness check per mode change)
- **Battery**: Positive impact (reduced screen power consumption)
