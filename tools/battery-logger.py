#!/usr/bin/env python3
"""
Battery Usage Logger
Logs battery statistics every 5 minutes for long-term analysis
"""

import time
import csv
import os
from datetime import datetime
from pathlib import Path

# Configuration
LOG_DIR = Path.home() / ".local/share/power-profile-manager/logs"
INTERVAL = 300  # 5 minutes in seconds

def read_file(path):
    """Read single line from file"""
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return None

def get_battery_info():
    """Get current battery information"""
    battery_path = "/sys/class/power_supply/BAT0"
    
    capacity = read_file(f"{battery_path}/capacity")
    status = read_file(f"{battery_path}/status")
    
    # Calculate discharge rate
    power_now = read_file(f"{battery_path}/power_now")
    if power_now:
        discharge_rate = float(power_now) / 1000000  # Convert to Watts
    else:
        discharge_rate = 0.0
    
    # Check AC status
    ac_online = read_file("/sys/class/power_supply/AC/online")
    
    return {
        'capacity': capacity or '?',
        'status': status or 'Unknown',
        'discharge_rate': f"{discharge_rate:.2f}",
        'ac_online': ac_online or '?'
    }

def get_power_mode():
    """Get current power profile mode"""
    try:
        epp = read_file("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference")
        if epp == "power":
            return "powersave"
        elif epp == "balance_power":
            return "balanced"
        elif epp == "balance_performance":
            return "performance"
        else:
            return epp or "unknown"
    except:
        return "unknown"

def get_top_process():
    """Get process using most CPU"""
    try:
        import subprocess
        result = subprocess.run(
            ['ps', 'aux', '--sort=-%cpu'],
            capture_output=True,
            text=True,
            timeout=2
        )
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            # Skip header, get first process
            fields = lines[1].split()
            if len(fields) >= 11:
                cpu_pct = fields[2]
                process = fields[10]
                return process, cpu_pct
    except:
        pass
    return "unknown", "0.0"

def log_battery_data():
    """Log current battery data to CSV"""
    # Create log directory if it doesn't exist
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Use daily log files
    log_file = LOG_DIR / f"battery-{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # Check if file exists to write header
    file_exists = log_file.exists()
    
    # Get data
    battery = get_battery_info()
    power_mode = get_power_mode()
    top_process, top_cpu = get_top_process()
    
    # Write to CSV
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        
        # Write header if new file
        if not file_exists:
            writer.writerow([
                'timestamp',
                'battery_pct',
                'status',
                'discharge_rate_w',
                'ac_online',
                'power_mode',
                'top_process',
                'top_cpu_pct'
            ])
        
        # Write data
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            battery['capacity'],
            battery['status'],
            battery['discharge_rate'],
            battery['ac_online'],
            power_mode,
            top_process,
            top_cpu
        ])

def main():
    """Main loop"""
    print(f"Battery Logger started")
    print(f"Logging to: {LOG_DIR}")
    print(f"Interval: {INTERVAL} seconds (5 minutes)")
    print(f"Press Ctrl+C to stop")
    
    try:
        while True:
            log_battery_data()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged battery data")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nBattery Logger stopped")

if __name__ == "__main__":
    main()
