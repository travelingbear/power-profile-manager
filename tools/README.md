# Battery Usage Logger

Track your laptop's battery usage over time and identify power-hungry applications.

## Features

- 📊 **Long-term tracking** - Logs battery data every 5 minutes
- 🔋 **Charge cycle analysis** - Track complete discharge cycles with duration and drop rate
- 📈 **Detailed statistics** - Battery drop rate, power consumption, estimated runtime
- 🎯 **Process impact analysis** - Identify which apps drain your battery the most
- 💡 **Smart recommendations** - Get actionable advice to improve battery life
- 🖥️ **GUI application** - Easy-to-use interface for control and analysis
- 📁 **CSV export** - Open logs in LibreOffice Calc or Excel for custom analysis

## Quick Start

### 1. Start Logging

**GUI (Recommended):**
```bash
python3 battery-logger-gui.py
```

**Command Line:**
```bash
python3 battery-logger.py
```

### 2. Analyze Data

```bash
./battery-analyze.sh
```

## Installation

### Requirements

- Python 3.6+
- Linux with sysfs battery interface
- GTK 3 (for GUI)

### Setup

```bash
# Clone or copy the tools directory
cd ~/Documents/PROJECTS/power-profile-manager/tools/

# Make scripts executable
chmod +x battery-logger.py battery-logger-gui.py battery-analyze.sh

# Optional: Install desktop entry
cp ~/.local/share/applications/battery-logger.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

## Usage

### Battery Logger

Logs battery data every 5 minutes to CSV files:

```bash
# Start logger
python3 battery-logger.py

# Run in background
nohup python3 battery-logger.py &

# Stop logger
pkill -f battery-logger.py
```

**Log location:** `~/.local/share/power-profile-manager/logs/`

**Log format:** `battery-YYYY-MM-DD.csv`

### GUI Application

Simple interface to control the logger:

```bash
python3 battery-logger-gui.py
```

Features:
- Start/Stop logger
- View current status
- Open log directory
- Run analysis report

### Analyzer

Generate detailed battery usage report:

```bash
./battery-analyze.sh
```

**Report includes:**
- Battery statistics (range, average, drop rate)
- Power consumption assessment (with benchmarks)
- Top battery-draining processes (with impact scores)
- Charge cycle analysis (duration, drop rate, timestamps)
- Power mode distribution
- AC vs battery time
- Smart recommendations

## CSV Format

```csv
timestamp,battery_pct,status,discharge_rate_w,ac_online,power_mode,top_process,top_cpu_pct
2025-12-07 22:00:00,95,Discharging,6.2,0,balanced,firefox,15.3
```

**Columns:**
- `timestamp` - Date and time
- `battery_pct` - Battery percentage (0-100)
- `status` - Charging, Discharging, Not charging, Full
- `discharge_rate_w` - Power consumption in Watts
- `ac_online` - 1=AC connected, 0=on battery
- `power_mode` - powersave, balanced, performance
- `top_process` - Process using most CPU
- `top_cpu_pct` - CPU usage of top process

## Example Analysis Output

```
═══════════════════════════════════════════════════════════════
  POWER CONSUMPTION
═══════════════════════════════════════════════════════════════
Average discharge rate: 5.97 W
Range: 5.62 W - 6.44 W

Assessment: GOOD (Normal for light usage)

Reference benchmarks:
  • Idle (screen dim):     2-3 W
  • Light work (browsing): 4-6 W
  • Active work (coding):  6-8 W
  • Heavy work (video):    8-12 W
  • Gaming/rendering:      12-20 W

Estimated battery life at 5.97 W:
  • 50 Wh battery: 8.4 hours
  • 60 Wh battery: 10.1 hours
  • 70 Wh battery: 11.7 hours

═══════════════════════════════════════════════════════════════
  CHARGE CYCLE ANALYSIS
═══════════════════════════════════════════════════════════════

Cycle #1:
  Started:  2025-12-07 08:00:00 at 95%
  Ended:    2025-12-07 14:30:00 at 15%
  Duration: 6.5 hours
  Drop:     80% (12.3% per hour)
  Avg Power: 6.8 W
```

## Advanced Usage

### Custom Analysis

```bash
# Average discharge rate
awk -F',' 'NR>1 && $5==0 {sum+=$4; count++} END {print sum/count " W"}' battery-*.csv

# Total time on battery
awk -F',' 'NR>1 && $5==0 {count++} END {print count*5 " minutes"}' battery-*.csv

# Most common process
awk -F',' 'NR>1 {print $7}' battery-*.csv | sort | uniq -c | sort -rn | head -1
```

### Open in Spreadsheet

```bash
libreoffice --calc ~/.local/share/power-profile-manager/logs/battery-*.csv
```

### Log Management

```bash
# Delete logs older than 30 days
find ~/.local/share/power-profile-manager/logs/ -name "battery-*.csv" -mtime +30 -delete

# Archive old logs
cd ~/.local/share/power-profile-manager/logs/
tar -czf archive-$(date +%Y%m).tar.gz battery-*.csv --mtime=+7
```

## Integration

Works alongside [Power Profile Manager](https://github.com/travelingbear/power-profile-manager):
- Logs power mode changes
- Tracks effectiveness of power profiles
- Identifies battery-draining applications
- Provides data for optimization

## Performance

- **CPU**: < 0.01% (runs every 5 minutes)
- **Memory**: ~5 MB
- **Disk**: ~20-40 KB per day (~1 MB per month)
- **Battery impact**: Negligible

## Troubleshooting

### Logger not running

```bash
ps aux | grep battery-logger
```

### No logs created

```bash
mkdir -p ~/.local/share/power-profile-manager/logs/
```

### Inaccurate data

Verify battery sysfs files:
```bash
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/power_now
```

## Tips

1. Run for at least 24 hours to get meaningful data
2. Compare different days to see usage patterns
3. Check after updates to see if new apps drain battery
4. Use with PowerTOP for detailed per-app analysis
5. Export to spreadsheet for advanced analysis

## License

GNU General Public License v3.0

## Author

Part of the Power Profile Manager project
