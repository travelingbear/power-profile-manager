#!/usr/bin/env python3
"""
Power Profile Manager - Configuration GUI
Simple GTK interface to edit /etc/power-profiled.conf
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import os

CONFIG_FILE = '/etc/power-profiled.conf'

class PowerProfileConfig(Gtk.Window):
    def __init__(self):
        super().__init__(title="Power Profile Manager - Configuration")
        self.set_border_width(20)
        self.set_default_size(500, 400)
        
        # Main container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Power Profile Manager</b></big>")
        vbox.pack_start(title, False, False, 0)
        
        # Current status
        self.status_label = Gtk.Label()
        self.update_status()
        vbox.pack_start(self.status_label, False, False, 0)
        
        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 0)
        
        # Configuration section
        config_label = Gtk.Label()
        config_label.set_markup("<b>Configuration</b>")
        config_label.set_halign(Gtk.Align.START)
        vbox.pack_start(config_label, False, False, 0)
        
        # Threshold setting
        threshold_box = Gtk.Box(spacing=10)
        threshold_label = Gtk.Label(label="Battery Threshold (%):")
        threshold_label.set_halign(Gtk.Align.START)
        threshold_box.pack_start(threshold_label, False, False, 0)
        
        self.threshold_spin = Gtk.SpinButton()
        self.threshold_spin.set_range(5, 99)
        self.threshold_spin.set_increments(5, 10)
        self.threshold_spin.set_value(self.read_config_value('THRESHOLD', 30))
        threshold_box.pack_start(self.threshold_spin, False, False, 0)
        
        threshold_help = Gtk.Label()
        threshold_help.set_markup("<small>Trigger ultra power-saving at this battery level</small>")
        threshold_help.set_halign(Gtk.Align.START)
        
        vbox.pack_start(threshold_box, False, False, 0)
        vbox.pack_start(threshold_help, False, False, 0)
        
        # Interval setting
        interval_box = Gtk.Box(spacing=10)
        interval_label = Gtk.Label(label="Check Interval (seconds):")
        interval_label.set_halign(Gtk.Align.START)
        interval_box.pack_start(interval_label, False, False, 0)
        
        self.interval_spin = Gtk.SpinButton()
        self.interval_spin.set_range(1, 600)
        self.interval_spin.set_increments(1, 10)
        self.interval_spin.set_value(self.read_config_value('INTERVAL', 60))
        interval_box.pack_start(self.interval_spin, False, False, 0)
        
        interval_help = Gtk.Label()
        interval_help.set_markup("<small>How often to check battery status</small>")
        interval_help.set_halign(Gtk.Align.START)
        
        vbox.pack_start(interval_box, False, False, 0)
        vbox.pack_start(interval_help, False, False, 0)
        
        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 0)
        
        # Brightness section
        brightness_label = Gtk.Label()
        brightness_label.set_markup("<b>Automatic Brightness Control</b>")
        brightness_label.set_halign(Gtk.Align.START)
        vbox.pack_start(brightness_label, False, False, 0)
        
        # Auto brightness toggle
        self.auto_brightness_check = Gtk.CheckButton(label="Enable automatic brightness adjustment")
        self.auto_brightness_check.set_active(self.read_config_value('AUTO_BRIGHTNESS', 0) == 1)
        self.auto_brightness_check.connect("toggled", self.on_auto_brightness_toggled)
        vbox.pack_start(self.auto_brightness_check, False, False, 0)
        
        # Brightness settings container
        self.brightness_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.brightness_box.set_margin_start(20)
        
        # Power Save brightness
        powersave_box = Gtk.Box(spacing=10)
        powersave_label = Gtk.Label(label="Power Save Mode (%):")
        powersave_label.set_halign(Gtk.Align.START)
        powersave_label.set_size_request(200, -1)
        powersave_box.pack_start(powersave_label, False, False, 0)
        
        self.brightness_powersave_spin = Gtk.SpinButton()
        self.brightness_powersave_spin.set_range(10, 100)
        self.brightness_powersave_spin.set_increments(5, 10)
        self.brightness_powersave_spin.set_value(self.read_config_value('BRIGHTNESS_POWERSAVE', 60))
        powersave_box.pack_start(self.brightness_powersave_spin, False, False, 0)
        
        self.brightness_box.pack_start(powersave_box, False, False, 0)
        
        # Balanced brightness
        balanced_box = Gtk.Box(spacing=10)
        balanced_label = Gtk.Label(label="Balanced Mode (%):")
        balanced_label.set_halign(Gtk.Align.START)
        balanced_label.set_size_request(200, -1)
        balanced_box.pack_start(balanced_label, False, False, 0)
        
        self.brightness_balanced_spin = Gtk.SpinButton()
        self.brightness_balanced_spin.set_range(10, 100)
        self.brightness_balanced_spin.set_increments(5, 10)
        self.brightness_balanced_spin.set_value(self.read_config_value('BRIGHTNESS_BALANCED', 80))
        balanced_box.pack_start(self.brightness_balanced_spin, False, False, 0)
        
        self.brightness_box.pack_start(balanced_box, False, False, 0)
        
        # Performance brightness
        performance_box = Gtk.Box(spacing=10)
        performance_label = Gtk.Label(label="Performance Mode (%):")
        performance_label.set_halign(Gtk.Align.START)
        performance_label.set_size_request(200, -1)
        performance_box.pack_start(performance_label, False, False, 0)
        
        self.brightness_performance_spin = Gtk.SpinButton()
        self.brightness_performance_spin.set_range(10, 100)
        self.brightness_performance_spin.set_increments(5, 10)
        self.brightness_performance_spin.set_value(self.read_config_value('BRIGHTNESS_PERFORMANCE', 100))
        performance_box.pack_start(self.brightness_performance_spin, False, False, 0)
        
        self.brightness_box.pack_start(performance_box, False, False, 0)
        
        brightness_help = Gtk.Label()
        brightness_help.set_markup("<small>Brightness is set once when entering each mode</small>")
        brightness_help.set_halign(Gtk.Align.START)
        self.brightness_box.pack_start(brightness_help, False, False, 0)
        
        vbox.pack_start(self.brightness_box, False, False, 0)
        
        # Set initial sensitivity
        self.on_auto_brightness_toggled(self.auto_brightness_check)
        
        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 0)
        
        # Buttons
        button_box = Gtk.Box(spacing=10)
        button_box.set_halign(Gtk.Align.END)
        
        save_button = Gtk.Button(label="Save & Restart")
        save_button.connect("clicked", self.on_save_clicked)
        button_box.pack_start(save_button, False, False, 0)
        
        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", lambda x: self.destroy())
        button_box.pack_start(cancel_button, False, False, 0)
        
        vbox.pack_start(button_box, False, False, 0)
        
    def read_config_value(self, key, default):
        try:
            with open(CONFIG_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#') or not line:
                        continue
                    if '=' in line and line.split('=')[0].strip() == key:
                        return int(line.split('=')[1].strip())
        except:
            pass
        return default
    
    def update_status(self):
        try:
            # Check daemon status
            daemon_status = subprocess.run(['systemctl', 'is-active', 'power-profiled'],
                                         capture_output=True, text=True)
            daemon_running = daemon_status.stdout.strip() == 'active'
            
            result = subprocess.run(['power-profile-ctl', 'status'], 
                                  capture_output=True, text=True)
            lines = result.stdout.split('\n')
            battery = next((l for l in lines if 'Battery:' in l), 'Battery: N/A')
            status = next((l for l in lines if 'Power Status:' in l), 'Status: N/A')
            profile = next((l for l in lines if 'Active Profile:' in l), 'Profile: N/A')
            
            daemon_text = "✓ Daemon: Running" if daemon_running else "✗ Daemon: STOPPED"
            daemon_color = "green" if daemon_running else "red"
            
            self.status_label.set_markup(
                f"<small><span color='{daemon_color}'><b>{daemon_text}</b></span>\n"
                f"{battery.strip()}\n{status.strip()}\n{profile.strip()}</small>"
            )
        except:
            self.status_label.set_text("Status unavailable")
    
    def on_auto_brightness_toggled(self, checkbox):
        """Enable/disable brightness controls based on checkbox"""
        is_active = checkbox.get_active()
        self.brightness_box.set_sensitive(is_active)
    
    def on_save_clicked(self, button):
        threshold = int(self.threshold_spin.get_value())
        interval = int(self.interval_spin.get_value())
        auto_brightness = 1 if self.auto_brightness_check.get_active() else 0
        brightness_powersave = int(self.brightness_powersave_spin.get_value())
        brightness_balanced = int(self.brightness_balanced_spin.get_value())
        brightness_performance = int(self.brightness_performance_spin.get_value())
        
        # Create new config content
        config_content = f"""# Power Profile Manager Configuration

# Battery threshold (percentage) to trigger ultra power-saving mode
# When battery drops to or below this level, powersave profile is applied
# Default: 30
THRESHOLD={threshold}

# Check interval in seconds
# How often the daemon checks battery status
# Default: 60
INTERVAL={interval}

# Automatic brightness control
# 0 = disabled, 1 = enabled
# Default: 0 (disabled)
AUTO_BRIGHTNESS={auto_brightness}

# Brightness levels for each power mode (percentage)
# Values: 10-100
# Brightness is set once when entering each mode

# Ultra Power Save mode (battery <= threshold)
# Default: 60
BRIGHTNESS_POWERSAVE={brightness_powersave}

# Balanced mode (battery > threshold, on battery)
# Default: 80
BRIGHTNESS_BALANCED={brightness_balanced}

# Performance mode (AC connected)
# Default: 100
BRIGHTNESS_PERFORMANCE={brightness_performance}
"""
        
        # Write config and restart daemon with single pkexec call
        try:
            # Write to temp file
            temp_file = '/tmp/power-profiled.conf.tmp'
            with open(temp_file, 'w') as f:
                f.write(config_content)
            
            # Create script to copy config and restart daemon
            script_file = '/tmp/power-profiled-update.sh'
            with open(script_file, 'w') as f:
                f.write(f"""#!/bin/bash
cp {temp_file} {CONFIG_FILE}
systemctl restart power-profiled
""")
            os.chmod(script_file, 0o755)
            
            # Execute with single pkexec call
            subprocess.run(['pkexec', script_file], check=True)
            
            # Cleanup
            os.remove(temp_file)
            os.remove(script_file)
            
            # Show success dialog
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Configuration Saved"
            )
            dialog.format_secondary_text(
                f"Threshold: {threshold}%\nInterval: {interval}s\n\nDaemon restarted successfully."
            )
            dialog.run()
            dialog.destroy()
            self.destroy()
            
        except Exception as e:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Error Saving Configuration"
            )
            dialog.format_secondary_text(str(e))
            dialog.run()
            dialog.destroy()

if __name__ == '__main__':
    win = PowerProfileConfig()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
