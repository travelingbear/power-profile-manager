#!/bin/bash
# Power Profile Manager - Argos Panel Indicator
# Refresh every 30 seconds

BATTERY_PATH="/sys/class/power_supply/BAT0"
AC_PATH="/sys/class/power_supply/AC"
STATE_FILE="/var/run/power-profile-state"
CONFIG_FILE="$HOME/.config/power-profile-manager/argos.conf"

# Load config (show percentage by default)
SHOW_PERCENTAGE=true
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Get battery info
LEVEL=$(cat "$BATTERY_PATH/capacity" 2>/dev/null || echo "?")
STATUS=$(cat "$BATTERY_PATH/status" 2>/dev/null || echo "Unknown")
AC_ONLINE=$(cat "$AC_PATH/online" 2>/dev/null || echo "0")
STATE=$(cat "$STATE_FILE" 2>/dev/null || echo "inactive")

# Determine icon and profile name based on AC status
if [[ "$AC_ONLINE" == "1" ]]; then
    ICON="🔌"
    PROFILE="Performance"
elif [[ "$STATE" == "powersave" ]]; then
    ICON="🪫"
    PROFILE="Power Save"
else
    ICON="🔋"
    PROFILE="Balanced"
fi

# Panel display
if [ "$SHOW_PERCENTAGE" = true ]; then
    echo "$ICON $LEVEL%"
else
    echo "$ICON"
fi
echo "---"

# Dropdown menu
echo "Power Profile Manager"
echo "---"

# Check daemon status
if systemctl is-active --quiet power-profiled; then
    echo "Daemon: Running"
else
    echo "Daemon: Stopped | bash='pkexec systemctl start power-profiled' terminal=false"
fi

# Check TLP status
if systemctl is-active --quiet tlp; then
    echo "TLP: Running"
else
    echo "TLP: Stopped | bash='pkexec systemctl start tlp' terminal=false"
fi

echo "---"
echo "Battery: $LEVEL% ($STATUS)"
echo "Active Profile: $PROFILE"
echo "---"

# CPU info
EPP=$(cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference 2>/dev/null || echo "N/A")
TURBO=$(cat /sys/devices/system/cpu/intel_pstate/no_turbo 2>/dev/null)
if [ "$TURBO" == "0" ]; then
    TURBO_STATUS="Enabled"
elif [ "$TURBO" == "1" ]; then
    TURBO_STATUS="Disabled"
else
    TURBO=$(cat /sys/devices/system/cpu/cpufreq/boost 2>/dev/null)
    TURBO_STATUS=$([ "$TURBO" == "1" ] && echo "Enabled" || echo "Disabled")
fi
PLATFORM=$(cat /sys/firmware/acpi/platform_profile 2>/dev/null || echo "N/A")

echo "CPU Settings:"
echo "  EPP: $EPP | size=11"
echo "  Turbo: $TURBO_STATUS | size=11"
echo "  Platform: $PLATFORM | size=11"
echo "---"

# Actions
echo "Configure | bash='python3 /usr/local/share/power-profile-manager/power-profile-config.py' terminal=false"
echo "Monitor | bash='gnome-terminal -- power-profile-ctl monitor' terminal=false"
echo "Restart Daemon | bash='pkexec systemctl restart power-profiled' terminal=false"
echo "---"

# Toggle percentage display
if [ "$SHOW_PERCENTAGE" = true ]; then
    echo "Hide Percentage | bash='mkdir -p ~/.config/power-profile-manager && echo \"SHOW_PERCENTAGE=false\" > ~/.config/power-profile-manager/argos.conf' terminal=false"
else
    echo "Show Percentage | bash='mkdir -p ~/.config/power-profile-manager && echo \"SHOW_PERCENTAGE=true\" > ~/.config/power-profile-manager/argos.conf' terminal=false"
fi

echo "---"
echo "View Logs | bash='gnome-terminal -- journalctl -u power-profiled -f' terminal=false"
echo "About | bash='zenity --info --text=\"Power Profile Manager v1.0.3\n\nDynamic power management for laptops\n\nhttps://github.com/travelingbear/power-profile-manager\"' terminal=false"
