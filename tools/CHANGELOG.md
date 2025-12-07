# Changelog - Battery Usage Logger

All notable changes to the Battery Usage Logger will be documented in this file.

## [1.0.0] - 2025-12-07

### Added
- Initial release of Battery Usage Logger
- Logs battery data every 5 minutes to CSV files
- Tracks battery percentage, discharge rate, power mode, and top process
- Daily log files with automatic rotation
- Comprehensive analysis script with detailed reports
- GUI application for easy control and monitoring
- Desktop entry for GNOME applications menu

### Features

#### Logger (battery-logger.py)
- Logs battery statistics every 5 minutes
- Captures battery level, status, discharge rate
- Records AC connection status
- Tracks active power mode (powersave/balanced/performance)
- Identifies top CPU-consuming process
- Creates daily CSV files
- Minimal resource usage (< 0.01% CPU, ~5 MB memory)

#### Analyzer (battery-analyze.sh)
- Battery statistics (range, average, drop rate)
- Power consumption analysis with assessment
- Reference benchmarks for context
- Battery life estimates for different capacities
- Process impact analysis (frequency × CPU usage)
- Charge cycle tracking with timestamps
- Duration and drop rate per cycle
- Estimated remaining time for ongoing cycles
- Power mode distribution
- AC vs battery time breakdown
- Smart recommendations based on usage patterns

#### GUI (battery-logger-gui.py)
- Start/Stop logger controls
- Real-time status display
- Log file count and entry count
- Open log directory button
- Run analysis report button
- Auto-refresh every 5 seconds
- GTK3 interface

### Technical Details
- Python 3.6+ compatible
- Uses sysfs for battery information
- CSV format for easy analysis
- Bash script for analysis (awk-based)
- GTK3 for GUI
- No external dependencies beyond standard library

### File Structure
```
tools/
├── battery-logger.py          # Main logger daemon
├── battery-logger-gui.py      # GUI application
├── battery-analyze.sh         # Analysis script
├── README.md                  # Documentation
└── CHANGELOG.md              # This file
```

### Log Format
```csv
timestamp,battery_pct,status,discharge_rate_w,ac_online,power_mode,top_process,top_cpu_pct
```

### Performance
- CPU usage: < 0.01%
- Memory: ~5 MB
- Disk: ~20-40 KB per day
- Battery impact: Negligible

### Known Limitations
- Requires Linux with sysfs battery interface
- Only tracks BAT0 (primary battery)
- 5-minute granularity (configurable in code)
- Charge cycle detection requires AC plug/unplug events

### Future Enhancements
- [ ] Configurable logging interval via GUI
- [ ] Multi-battery support
- [ ] Export reports to PDF
- [ ] Historical comparison (week-over-week)
- [ ] Battery health tracking
- [ ] Integration with system notifications
- [ ] Web dashboard for remote monitoring

## Installation

See README.md for installation instructions.

## Usage

```bash
# Start logger
python3 battery-logger.py

# Open GUI
python3 battery-logger-gui.py

# Analyze data
./battery-analyze.sh
```

## License

GNU General Public License v3.0
