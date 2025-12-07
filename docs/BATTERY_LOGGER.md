# Battery Usage Logger

## Overview

A lightweight tool to track battery usage over time (hours, days, weeks) and identify which applications consume the most power.

## Features

- Logs battery data every 5 minutes
- Tracks battery percentage, discharge rate, power mode
- Records top CPU-consuming process
- Creates daily CSV files for easy analysis
- Minimal overhead (< 0.01% CPU, < 5 MB memory)
- Built-in analyzer for quick statistics

## Installation

### Manual Start (Testing)

```bash
# Start logger in terminal
~/Documents/PROJECTS/power-profile-manager/tools/battery-logger.py

# Or run in background
nohup ~/Documents/PROJECTS/power-profile-manager/tools/battery-logger.py &
```

### Auto-Start on Login (Recommended)

Add to startup applications:

1. Open "Startup Applications"
2. Click "Add"
3. Name: Battery Logger
4. Command: `/usr/bin/python3 /home/francisco/Documents/PROJECTS/power-profile-manager/tools/battery-logger.py`
5. Click "Add"

### Systemd Service (Advanced)

```bash
# Install
sudo cp ~/Documents/PROJECTS/power-profile-manager/tools/battery-logger.py /usr/local/bin/
sudo cp ~/Documents/PROJECTS/power-profile-manager/tools/battery-logger.service /etc/systemd/user/

# Enable and start
systemctl --user enable battery-logger.service
systemctl --user start battery-logger.service

# Check status
systemctl --user status battery-logger.service
```

## Usage

### View Logs

Logs are stored in: `~/.local/share/power-profile-manager/logs/`

Each day creates a new file: `battery-YYYY-MM-DD.csv`

### Analyze Logs

```bash
# Quick analysis
~/Documents/PROJECTS/power-profile-manager/tools/battery-analyze.sh

# View raw data
cat ~/.local/share/power-profile-manager/logs/battery-$(date +%Y-%m-%d).csv

# Open in LibreOffice Calc
libreoffice --calc ~/.local/share/power-profile-manager/logs/battery-*.csv
```

### Example Analysis Output

```
=== Battery Usage Analysis ===
Log file: battery-2025-12-07.csv

Total entries: 144
Time range: 2025-12-07 08:00:00 to 2025-12-07 20:00:00

=== Battery Statistics ===
Battery range: 45% - 95%
Average battery: 72.3%
Battery drop: 50%

=== Power Consumption ===
Average discharge rate: 6.15 W

=== Top Battery-Draining Processes ===
     45 firefox
     32 code
     28 gnome-shell
     15 chrome
     12 spotify

=== Power Mode Distribution ===
     89 balanced
     42 powersave
     13 performance

=== AC vs Battery Time ===
On AC: 48 entries (33.3%)
On Battery: 96 entries (66.7%)
```

## CSV Format

```csv
timestamp,battery_pct,status,discharge_rate_w,ac_online,power_mode,top_process,top_cpu_pct
2025-12-07 22:00:00,95,Discharging,6.2,0,balanced,firefox,15.3
2025-12-07 22:05:00,94,Discharging,6.1,0,balanced,code,12.1
```

### Columns

- **timestamp**: Date and time of measurement
- **battery_pct**: Battery percentage (0-100)
- **status**: Charging, Discharging, Not charging, Full
- **discharge_rate_w**: Power consumption in Watts
- **ac_online**: 1 = AC connected, 0 = on battery
- **power_mode**: powersave, balanced, performance
- **top_process**: Process using most CPU
- **top_cpu_pct**: CPU usage percentage of top process

## Data Analysis

### Using LibreOffice Calc

1. Open CSV file in Calc
2. Create charts:
   - Battery % over time (line chart)
   - Discharge rate over time (line chart)
   - Process frequency (pie chart)
   - Power mode distribution (bar chart)

### Using Command Line

```bash
# Average discharge rate
awk -F',' 'NR>1 && $5==0 {sum+=$4; count++} END {print sum/count " W"}' battery-*.csv

# Total time on battery (in 5-min intervals)
awk -F',' 'NR>1 && $5==0 {count++} END {print count*5 " minutes"}' battery-*.csv

# Most common process
awk -F',' 'NR>1 {print $7}' battery-*.csv | sort | uniq -c | sort -rn | head -1
```

## File Management

### Log Rotation

Logs are automatically created daily. Old logs are kept indefinitely.

To clean old logs:

```bash
# Delete logs older than 30 days
find ~/.local/share/power-profile-manager/logs/ -name "battery-*.csv" -mtime +30 -delete

# Archive logs older than 7 days
cd ~/.local/share/power-profile-manager/logs/
tar -czf archive-$(date +%Y%m).tar.gz battery-*.csv --mtime=+7
find . -name "battery-*.csv" -mtime +7 -delete
```

### Disk Usage

- ~20-40 KB per day
- ~1 MB per month
- ~12 MB per year

## Troubleshooting

### Logger Not Running

Check if process is running:
```bash
ps aux | grep battery-logger
```

### No Logs Created

Check permissions:
```bash
ls -la ~/.local/share/power-profile-manager/logs/
```

Create directory if missing:
```bash
mkdir -p ~/.local/share/power-profile-manager/logs/
```

### Inaccurate Data

Ensure battery sysfs files are accessible:
```bash
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/power_now
```

## Integration with Power Profile Manager

The logger works alongside your power-profile-manager:
- Logs power mode changes
- Tracks effectiveness of power profiles
- Helps identify battery-draining applications
- Provides data for optimization

## Performance Impact

- **CPU**: < 0.01% (runs every 5 minutes)
- **Memory**: ~5 MB
- **Disk I/O**: Minimal (one write every 5 minutes)
- **Battery**: Negligible impact

## Tips

1. **Run for at least 24 hours** to get meaningful data
2. **Compare different days** to see usage patterns
3. **Check after updates** to see if new apps drain battery
4. **Use with PowerTOP** for detailed per-app analysis
5. **Export to spreadsheet** for advanced analysis

## Uninstall

```bash
# Stop logger
pkill -f battery-logger.py

# Remove files
rm -rf ~/.local/share/power-profile-manager/logs/
rm ~/Documents/PROJECTS/power-profile-manager/tools/battery-logger.py

# If using systemd
systemctl --user stop battery-logger.service
systemctl --user disable battery-logger.service
rm /etc/systemd/user/battery-logger.service
```
