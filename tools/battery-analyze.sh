#!/bin/bash
# Battery Log Analyzer
# Analyzes battery usage logs with detailed insights

LOG_DIR="$HOME/.local/share/power-profile-manager/logs"

if [ ! -d "$LOG_DIR" ]; then
    echo "No logs found at $LOG_DIR"
    exit 1
fi

# Find latest log file
LATEST_LOG=$(ls -t "$LOG_DIR"/battery-*.csv 2>/dev/null | head -1)

if [ -z "$LATEST_LOG" ]; then
    echo "No log files found"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           BATTERY USAGE ANALYSIS REPORT                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo
echo "Log file: $LATEST_LOG"
echo

# Count entries
ENTRIES=$(tail -n +2 "$LATEST_LOG" | wc -l)
echo "Total entries: $ENTRIES"

# Time range
FIRST_TIME=$(tail -n +2 "$LATEST_LOG" | head -1 | cut -d',' -f1)
LAST_TIME=$(tail -n +2 "$LATEST_LOG" | tail -1 | cut -d',' -f1)
echo "Time range: $FIRST_TIME to $LAST_TIME"
echo

# Battery statistics
echo "═══════════════════════════════════════════════════════════════"
echo "  BATTERY STATISTICS"
echo "═══════════════════════════════════════════════════════════════"
tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN {
    min=100; max=0; sum=0; count=0;
}
{
    if ($2 != "?") {
        bat = $2 + 0;
        if (bat < min) min = bat;
        if (bat > max) max = bat;
        sum += bat;
        count++;
    }
}
END {
    if (count > 0) {
        printf "Battery range: %d%% - %d%%\n", min, max;
        printf "Average battery: %.1f%%\n", sum/count;
        drop = max - min;
        printf "Battery drop: %d%%\n", drop;
        
        # Estimate runtime
        if (drop > 0) {
            hours = (count * 5) / 60.0;  # 5 min intervals to hours
            rate = drop / hours;
            remaining = min / rate;
            printf "Discharge rate: %.1f%% per hour\n", rate;
            printf "Estimated remaining: %.1f hours at current rate\n", remaining;
        }
    }
}'
echo

# Power consumption with context
echo "═══════════════════════════════════════════════════════════════"
echo "  POWER CONSUMPTION"
echo "═══════════════════════════════════════════════════════════════"
tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN { sum=0; count=0; min=999; max=0; }
{
    if ($4 != "0.00" && $5 == "0") {  # Only when on battery
        rate = $4 + 0;
        sum += rate;
        if (rate < min) min = rate;
        if (rate > max) max = rate;
        count++;
    }
}
END {
    if (count > 0) {
        avg = sum/count;
        printf "Average discharge rate: %.2f W\n", avg;
        printf "Range: %.2f W - %.2f W\n", min, max;
        printf "\n";
        
        # Provide context
        printf "Assessment: ";
        if (avg < 4.0)
            printf "EXCELLENT (Very efficient)\n";
        else if (avg < 6.0)
            printf "GOOD (Normal for light usage)\n";
        else if (avg < 8.0)
            printf "MODERATE (Typical for active usage)\n";
        else if (avg < 10.0)
            printf "HIGH (Heavy workload or inefficient apps)\n";
        else
            printf "VERY HIGH (Check for power-hungry processes)\n";
        
        printf "\n";
        printf "Reference benchmarks:\n";
        printf "  • Idle (screen dim):     2-3 W\n";
        printf "  • Light work (browsing): 4-6 W\n";
        printf "  • Active work (coding):  6-8 W\n";
        printf "  • Heavy work (video):    8-12 W\n";
        printf "  • Gaming/rendering:      12-20 W\n";
        printf "\n";
        
        # Battery life estimate
        printf "Estimated battery life at %.2f W:\n", avg;
        # Assuming typical 50Wh battery
        printf "  • 50 Wh battery: %.1f hours\n", 50/avg;
        printf "  • 60 Wh battery: %.1f hours\n", 60/avg;
        printf "  • 70 Wh battery: %.1f hours\n", 70/avg;
    }
}'
echo

# Top processes with CPU usage
echo "═══════════════════════════════════════════════════════════════"
echo "  TOP BATTERY-DRAINING PROCESSES"
echo "═══════════════════════════════════════════════════════════════"
echo "Process                Count    Avg CPU%    Impact"
echo "───────────────────────────────────────────────────────────────"
tail -n +2 "$LATEST_LOG" | awk -F',' '
{
    if ($7 != "" && $7 != "unknown") {
        proc = $7;
        cpu = $8 + 0;
        count[proc]++;
        cpu_sum[proc] += cpu;
    }
}
END {
    for (proc in count) {
        avg_cpu = cpu_sum[proc] / count[proc];
        # Calculate impact score (frequency * avg CPU)
        impact = (count[proc] * avg_cpu) / 100;
        printf "%-20s %5d    %6.1f%%    %6.1f\n", proc, count[proc], avg_cpu, impact;
    }
}' | sort -k4 -rn | head -10
echo
echo "Impact = Frequency × Average CPU usage"
echo "Higher impact = More battery drain"
echo

# Power mode distribution
echo "═══════════════════════════════════════════════════════════════"
echo "  POWER MODE DISTRIBUTION"
echo "═══════════════════════════════════════════════════════════════"
tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN { total=0; }
{
    mode = $6;
    count[mode]++;
    total++;
}
END {
    for (mode in count) {
        pct = (count[mode] / total) * 100;
        printf "%-15s: %3d entries (%.1f%%)\n", mode, count[mode], pct;
    }
}' | sort -k2 -rn
echo

# Time on battery vs AC
echo "═══════════════════════════════════════════════════════════════"
echo "  AC vs BATTERY TIME"
echo "═══════════════════════════════════════════════════════════════"
tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN { ac=0; bat=0; }
{
    if ($5 == "1") ac++;
    else if ($5 == "0") bat++;
}
END {
    total = ac + bat;
    if (total > 0) {
        ac_hours = (ac * 5) / 60.0;
        bat_hours = (bat * 5) / 60.0;
        printf "On AC:      %3d entries (%.1f%%) = %.1f hours\n", ac, (ac/total)*100, ac_hours;
        printf "On Battery: %3d entries (%.1f%%) = %.1f hours\n", bat, (bat/total)*100, bat_hours;
    }
}'
echo

# Recommendations
echo "═══════════════════════════════════════════════════════════════"
echo "  RECOMMENDATIONS"
echo "═══════════════════════════════════════════════════════════════"

# Analyze and provide recommendations
tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN { 
    sum=0; count=0; 
    proc_count["firefox"]=0; proc_count["chrome"]=0; proc_count["code"]=0;
}
{
    if ($4 != "0.00" && $5 == "0") {
        sum += $4;
        count++;
    }
    proc = tolower($7);
    if (proc ~ /firefox/) proc_count["firefox"]++;
    if (proc ~ /chrome/) proc_count["chrome"]++;
    if (proc ~ /code/) proc_count["code"]++;
}
END {
    if (count > 0) {
        avg = sum/count;
        
        if (avg > 8.0)
            print "• High power consumption detected. Consider:";
        
        if (proc_count["firefox"] > 10)
            print "  - Firefox is frequently active. Close unused tabs.";
        if (proc_count["chrome"] > 10)
            print "  - Chrome/Chromium detected. Consider using fewer extensions.";
        if (proc_count["code"] > 10)
            print "  - VS Code active. Disable unused extensions.";
        
        if (avg > 6.0)
            print "• Enable power-save mode when not doing intensive work";
        
        if (avg < 5.0)
            print "• Excellent power efficiency! Current setup is optimal.";
    }
}'
echo

# Charge cycle analysis
echo "═══════════════════════════════════════════════════════════════"
echo "  CHARGE CYCLE ANALYSIS"
echo "═══════════════════════════════════════════════════════════════"

tail -n +2 "$LATEST_LOG" | awk -F',' '
BEGIN {
    cycle = 0;
    in_discharge = 0;
    max_bat = 0;
    min_bat = 100;
}
{
    timestamp = $1;
    battery = $2 + 0;
    status = $3;
    discharge_rate = $4 + 0;
    ac = $5 + 0;
    
    # Detect start of discharge cycle (unplugged or started discharging)
    if (ac == 0 && prev_ac == 1) {
        # Started new discharge cycle
        if (in_discharge && max_bat > 0) {
            # Print previous cycle
            cycle++;
            duration = (end_time - start_time) / 60.0;  # Assume 5 min intervals
            drop = max_bat - min_bat;
            rate = drop / (duration / 60.0);
            
            printf "\nCycle #%d:\n", cycle;
            printf "  Started:  %s at %d%%\n", start_timestamp, max_bat;
            printf "  Ended:    %s at %d%%\n", end_timestamp, min_bat;
            printf "  Duration: %.1f hours\n", duration / 60.0;
            printf "  Drop:     %d%% (%.1f%% per hour)\n", drop, rate;
            if (avg_discharge > 0)
                printf "  Avg Power: %.2f W\n", avg_discharge / discharge_count;
        }
        
        # Start new cycle
        in_discharge = 1;
        max_bat = battery;
        min_bat = battery;
        start_timestamp = timestamp;
        start_time = NR;
        avg_discharge = 0;
        discharge_count = 0;
    }
    
    # Track discharge cycle
    if (in_discharge && ac == 0) {
        if (battery > max_bat) max_bat = battery;
        if (battery < min_bat) min_bat = battery;
        end_timestamp = timestamp;
        end_time = NR;
        
        if (discharge_rate > 0) {
            avg_discharge += discharge_rate;
            discharge_count++;
        }
    }
    
    # Detect end of discharge (plugged in)
    if (ac == 1 && prev_ac == 0 && in_discharge) {
        # Cycle ended
        cycle++;
        duration = (end_time - start_time) * 5;  # 5 min intervals
        drop = max_bat - min_bat;
        rate = drop / (duration / 60.0);
        
        printf "\nCycle #%d:\n", cycle;
        printf "  Started:  %s at %d%%\n", start_timestamp, max_bat;
        printf "  Ended:    %s at %d%%\n", end_timestamp, min_bat;
        printf "  Duration: %.1f hours\n", duration / 60.0;
        printf "  Drop:     %d%% (%.1f%% per hour)\n", drop, rate;
        if (discharge_count > 0)
            printf "  Avg Power: %.2f W\n", avg_discharge / discharge_count;
        
        in_discharge = 0;
    }
    
    prev_ac = ac;
}
END {
    # Print last cycle if still discharging
    if (in_discharge && max_bat > 0) {
        cycle++;
        duration = (end_time - start_time) * 5;
        drop = max_bat - min_bat;
        rate = drop / (duration / 60.0);
        
        printf "\nCycle #%d: (ONGOING)\n", cycle;
        printf "  Started:  %s at %d%%\n", start_timestamp, max_bat;
        printf "  Current:  %s at %d%%\n", end_timestamp, min_bat;
        printf "  Duration: %.1f hours so far\n", duration / 60.0;
        printf "  Drop:     %d%% (%.1f%% per hour)\n", drop, rate;
        if (discharge_count > 0)
            printf "  Avg Power: %.2f W\n", avg_discharge / discharge_count;
        
        # Estimate remaining time
        if (rate > 0) {
            remaining = min_bat / rate;
            printf "  Estimated remaining: %.1f hours\n", remaining;
        }
    }
    
    if (cycle == 0) {
        print "\nNo complete discharge cycles found yet.";
        print "Keep logging to track full battery cycles.";
    }
}'
echo
echo "═══════════════════════════════════════════════════════════════"

