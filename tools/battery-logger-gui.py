#!/usr/bin/env python3
"""
Battery Logger GUI
Simple interface to control and view battery logging
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess
import os
from pathlib import Path

LOG_DIR = Path.home() / ".local/share/power-profile-manager/logs"
PID_FILE = Path.home() / ".local/share/power-profile-manager/battery-logger.pid"
LOGGER_SCRIPT = Path.home() / "Documents/PROJECTS/power-profile-manager/tools/battery-logger.py"

class BatteryLoggerGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Battery Logger")
        self.set_border_width(20)
        self.set_default_size(500, 400)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)
        
        # Title
        title = Gtk.Label()
        title.set_markup("<big><b>Battery Usage Logger</b></big>")
        vbox.pack_start(title, False, False, 0)
        
        # Status
        self.status_label = Gtk.Label()
        vbox.pack_start(self.status_label, False, False, 0)
        
        # Separator
        vbox.pack_start(Gtk.Separator(), False, False, 0)
        
        # Buttons
        button_box = Gtk.Box(spacing=10)
        
        self.start_button = Gtk.Button(label="Start Logger")
        self.start_button.connect("clicked", self.on_start_clicked)
        button_box.pack_start(self.start_button, True, True, 0)
        
        self.stop_button = Gtk.Button(label="Stop Logger")
        self.stop_button.connect("clicked", self.on_stop_clicked)
        button_box.pack_start(self.stop_button, True, True, 0)
        
        vbox.pack_start(button_box, False, False, 0)
        
        # Update status after buttons are created
        self.update_status()
        
        # Actions
        action_box = Gtk.Box(spacing=10)
        
        view_logs_btn = Gtk.Button(label="View Logs")
        view_logs_btn.connect("clicked", self.on_view_logs_clicked)
        action_box.pack_start(view_logs_btn, True, True, 0)
        
        analyze_btn = Gtk.Button(label="Analyze Data")
        analyze_btn.connect("clicked", self.on_analyze_clicked)
        action_box.pack_start(analyze_btn, True, True, 0)
        
        vbox.pack_start(action_box, False, False, 0)
        
        # Info
        info_label = Gtk.Label()
        info_label.set_markup(
            "<small>Logs battery usage every 5 minutes\n"
            f"Log directory: {LOG_DIR}</small>"
        )
        vbox.pack_start(info_label, False, False, 0)
        
        # Update status every 5 seconds
        GLib.timeout_add_seconds(5, self.update_status)
        
    def is_running(self):
        """Check if logger is running"""
        if not PID_FILE.exists():
            return False
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)  # Check if process exists
            return True
        except:
            return False
    
    def update_status(self):
        """Update status display"""
        running = self.is_running()
        
        if running:
            status_text = "✓ Logger: <span color='green'><b>Running</b></span>"
            self.start_button.set_sensitive(False)
            self.stop_button.set_sensitive(True)
        else:
            status_text = "✗ Logger: <span color='red'><b>Stopped</b></span>"
            self.start_button.set_sensitive(True)
            self.stop_button.set_sensitive(False)
        
        # Count log files
        if LOG_DIR.exists():
            log_files = list(LOG_DIR.glob("battery-*.csv"))
            status_text += f"\n\nLog files: {len(log_files)}"
            
            if log_files:
                latest = max(log_files, key=lambda p: p.stat().st_mtime)
                lines = len(latest.read_text().split('\n')) - 2  # Exclude header and empty line
                status_text += f"\nToday's entries: {lines}"
        
        self.status_label.set_markup(status_text)
        return True  # Continue timeout
    
    def on_start_clicked(self, button):
        """Start logger"""
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = Path.home() / ".local/share/power-profile-manager/battery-logger.log"
            
            # Start logger in background
            process = subprocess.Popen(
                ['python3', str(LOGGER_SCRIPT)],
                stdout=open(log_file, 'w'),
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
            
            # Save PID
            PID_FILE.write_text(str(process.pid))
            
            self.update_status()
            self.show_message("Logger started successfully")
        except Exception as e:
            self.show_error(f"Failed to start logger: {e}")
    
    def on_stop_clicked(self, button):
        """Stop logger"""
        try:
            if PID_FILE.exists():
                pid = int(PID_FILE.read_text().strip())
                os.kill(pid, 15)  # SIGTERM
                PID_FILE.unlink()
                self.update_status()
                self.show_message("Logger stopped")
        except Exception as e:
            self.show_error(f"Failed to stop logger: {e}")
    
    def on_view_logs_clicked(self, button):
        """Open log directory"""
        subprocess.Popen(['xdg-open', str(LOG_DIR)])
    
    def on_analyze_clicked(self, button):
        """Run analyzer in terminal"""
        analyzer = Path.home() / "Documents/PROJECTS/power-profile-manager/tools/battery-analyze.sh"
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'{analyzer}; read -p "Press Enter to close..."'])
    
    def show_message(self, message):
        """Show info message"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()
    
    def show_error(self, message):
        """Show error message"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    win = BatteryLoggerGUI()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
