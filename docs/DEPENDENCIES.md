# Dependencies

## Core System (Required)

### Build Dependencies
- GCC compiler
- make
- Standard C library (glibc)

### Runtime Dependencies
- Linux kernel 4.0+ with sysfs support
- systemd
- TLP (power management tool)

**Installation:**
```bash
# Debian/Ubuntu
sudo apt install build-essential tlp tlp-rdw

# Fedora
sudo dnf install gcc make tlp tlp-rdw

# Arch
sudo pacman -S base-devel tlp
```

## GUI Components (Optional)

### Argos GNOME Extension
**Purpose:** Top panel indicator showing battery and profile status

**Requirements:**
- GNOME Shell 3.36 or newer
- Argos extension v3.x

**Installation:**
1. Visit https://extensions.gnome.org/extension/1176/argos/
2. Click "Install" button
3. Enable the extension

**OR via command line:**
```bash
# Check GNOME Shell version
gnome-shell --version

# Install Argos
cd /tmp
wget https://extensions.gnome.org/extension-data/argospew.worldwidemann.com.v3.shell-extension.zip
gnome-extensions install argospew.worldwidemann.com.v3.shell-extension.zip
gnome-extensions enable argos@pew.worldwidemann.com

# Verify
gnome-extensions list | grep argos
```

**Restart GNOME Shell:**
- Press `Alt+F2`
- Type `r` and press `Enter`

### GTK Configuration GUI
**Purpose:** Graphical interface to edit configuration

**Requirements:**
- Python 3.6+
- GTK 3
- Python GObject bindings (PyGObject)
- pkexec (polkit)
- zenity (for dialogs)

**Installation:**
```bash
# Debian/Ubuntu
sudo apt install python3-gi gir1.2-gtk-3.0 policykit-1 zenity

# Fedora
sudo dnf install python3-gobject gtk3 polkit zenity

# Arch
sudo pacman -S python-gobject gtk3 polkit zenity
```

**Verify:**
```bash
python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk; print('GTK available')"
which pkexec
which zenity
```

## Dependency Summary

| Component | Required | Purpose |
|-----------|----------|---------|
| GCC | Yes | Build daemon |
| systemd | Yes | Service management |
| TLP | Yes | AC/battery power management |
| Argos | No | Panel indicator |
| Python GTK | No | Configuration GUI |
| pkexec | No | GUI privilege elevation |
| zenity | No | GUI dialogs |

## Minimal Installation (No GUI)

For servers or minimal systems, only install core dependencies:

```bash
# Install build tools and TLP
sudo apt install build-essential tlp tlp-rdw

# Build and install daemon only
cd ~/Documents/PROJECTS/power-profile-manager/src
./install.sh

# Use CLI tools only
power-profile-ctl status
power-profile-ctl monitor
```

## Troubleshooting Dependencies

### Check if TLP is installed
```bash
which tlp
systemctl status tlp
```

### Check if Argos is installed
```bash
gnome-extensions list | grep argos
ls ~/.local/share/gnome-shell/extensions/ | grep argos
```

### Check Python GTK
```bash
python3 -c "import gi; gi.require_version('Gtk', '3.0')"
```

### Check pkexec
```bash
which pkexec
pkexec --version
```

## Version Compatibility

| Component | Minimum Version | Tested Version |
|-----------|----------------|----------------|
| Linux Kernel | 4.0 | 6.x |
| GNOME Shell | 3.36 | 45.x |
| Python | 3.6 | 3.11 |
| GTK | 3.0 | 3.24 |
| TLP | 1.3 | 1.6 |
| systemd | 230 | 255 |
