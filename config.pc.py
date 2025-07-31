from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Wlan, Bluetooth
import subprocess

mod = "mod4"
terminal = "kitty fish"

colors = {
    "silver": "#e0e0e0",
    "chrome": "#ffffff",
    "metal": "#a0a0a0",
    "gunmetal": "#2a3439",
}

@hook.subscribe.startup_once
def start_picom():
    subprocess.Popen(["picom"])

@hook.subscribe.startup
def set_wallpaper():
    # Update this path to your desktop wallpaper directory
    subprocess.Popen(["feh", "--bg-fill", "/home/ch/Pictures/Wallpapers"])

@hook.subscribe.startup_once
def start_nmapplet():
    subprocess.Popen(["nm-applet"])

@hook.subscribe.startup_once
def monitors():
    subprocess.run(["xrandr", "--output", "DP-0", "--rate", "165"])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Random Hotkeys
    Key([mod], "d", lazy.spawn(
    "rofi -show drun "
    "-theme /usr/share/rofi/themes/android_notification.rasi "
    "-theme-str '"
    "window { width: 45%; background-color: #2a3439; border-color: #5e7c8a; } "
    "element { background-color: #2a3439; text-color: #e0e0e0; } "
    "element selected { background-color: #5e7c8a; text-color: #ffffff; }"
    "'"
), desc="Android-style launcher"),
    Key([mod], "Escape", lazy.spawn("/home/ch/.config/qtile/powermenu.sh"), desc="Show power menu"),
    # Desktop doesn't need brightness controls, but you can keep these if you have external monitors that support it
    # Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    
    # Volume controls (more relevant for desktop)
    #Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    #Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    #Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus=colors["silver"],  # Light gray focus border
        border_normal=colors["gunmetal"],  # Dark normal border
        border_width=2,  # Thinner borders (reduced from 4)
        margin=6,
        border_radius=3,
    ),
    layout.Max(
        border_focus=colors["silver"],  # Light gray focus border
        border_normal=colors["gunmetal"],  # Dark normal border 
        border_width=2,  # Thinner borders (reduced from 4)
        margin=6,
        border_radius=3,
    ),


    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # Left side
                widget.Spacer(length=8),
                widget.GroupBox(
                    active=colors["chrome"],
                    inactive=colors["metal"],
                    highlight_method="block",
                    this_current_screen_border=colors["silver"],
                    urgent_alert_method="block",
                    fontsize=14,
                    padding_x=8,
                    spacing=4,
                ),
                widget.Spacer(length=8),
                
                # Center-aligned window name
                widget.WindowName(
                    foreground=colors["chrome"],
                    font="JetBrainsMono Nerd Font Mono",
                    max_chars=50,
                    padding=10,
                ),
                
                # Right side - system info (desktop optimized)
                widget.Spacer(length=8),
                
                # Network status (Ethernet for desktop)
                widget.TextBox(
                     text="NET:",
                     foreground=colors["chrome"],
                     padding=5
                     ),
                widget.GenPollText(
                    foreground=colors["chrome"],
                    update_interval=5,
                    func=lambda: get_network_status(),
                    padding=5
                    ),
                widget.Spacer(length=8),

                # Bluetooth widget (optional for desktop)
                widget.TextBox(
                    text='BT:',
                    foreground=colors["chrome"],
                    padding=5,
                ),
                widget.GenPollText(
                    foreground=colors["chrome"],
                    update_interval=5,
                    func=lambda: get_bt_status(),
                    padding=5
                ),

                widget.Spacer(length=8),
                
                # Temperature monitoring using GenPollText
                widget.TextBox(
                    text='TEMP:',
                    foreground=colors["chrome"],
                    padding=5,
                ),
                widget.GenPollText(
                    foreground=colors["chrome"],
                    update_interval=5,
                    func=lambda: get_cpu_temp(),
                    padding=5
                ),
                
                widget.Spacer(length=8),
                
                # CPU usage using GenPollText
                widget.TextBox(
                    text='CPU:',
                    foreground=colors["chrome"],
                    padding=5,
                ),
                widget.GenPollText(
                    foreground=colors["chrome"],
                    update_interval=2,
                    func=lambda: get_cpu_usage(),
                    padding=5
                ),
                
                widget.Spacer(length=8),
                
                # Memory usage using GenPollText
                widget.TextBox(
                    text='RAM:',
                    foreground=colors["chrome"],
                    padding=5,
                ),
                widget.GenPollText(
                    foreground=colors["chrome"],
                    update_interval=2,
                    func=lambda: get_memory_usage(),
                    padding=5
                ),
                #widget.Spacer(length=8),
                
                # Volume widget (more useful for desktop) removed not necessary
                #widget.Volume(
                #    foreground=colors["chrome"],
                #    format='VOL: {percent}%',
                #    padding=5,
                #),
                
                # Battery widget removed for desktop
                # widget.Battery(
                #     foreground=colors["chrome"],
                #     format='BAT: {char} {percent:2.0%}',
                #     charge_char=' ',
                #     update_interval=10,
                # ),
                widget.Spacer(length=8),
                widget.Clock(
                    foreground=colors["chrome"],
                    format='%H:%M:%S',
                    padding=5,
                ),
                widget.Spacer(length=8),
            ],
            size=32,
            background=colors["gunmetal"] + "60",
            margin=[6, 6, 0, 6],
            opacity=0.9,
            border_radius=[5, 5, 0, 0],  # Only round top corners
        ),
    ),
]

def get_network_status():
    """Get network status - prioritizes ethernet over WiFi for desktop"""
    try:
        # Check ethernet connection first
        eth_result = subprocess.run(
            ["nmcli", "-t", "-f", "type,state", "con", "show", "--active"],
            capture_output=True, 
            text=True,
            check=True
        )
        
        for line in eth_result.stdout.splitlines():
            if "ethernet:activated" in line.lower():
                return "ETH"
        
        # If no ethernet, check WiFi
        wifi_result = subprocess.run(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
            capture_output=True, 
            text=True,
            check=True
        )
        
        for line in wifi_result.stdout.splitlines():
            if line.startswith("yes:"):
                return line.split(":")[1][:8]  # Return first 8 chars of SSID
            
        return "OFF"
    
    except subprocess.CalledProcessError:
        return "ERR"
    except Exception:
        return "N/A"

def get_cpu_temp():
    """Get CPU temperature"""
    try:
        result = subprocess.run(
            ["sensors"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Look for CPU temperature in sensors output
        for line in result.stdout.splitlines():
            if "Package id 0" in line or "Tctl" in line or "temp1" in line:
                # Extract temperature value
                temp_match = line.split("+")[1].split("°")[0] if "+" in line else None
                if temp_match:
                    return f"{float(temp_match):.0f}°C"
        
        # Fallback: try thermal zone
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read().strip()) / 1000
            return f"{temp:.0f}°C"
            
    except:
        return "N/A"

def get_cpu_usage():
    """Get CPU usage percentage"""
    try:
        # Use a simpler approach with vmstat
        result = subprocess.run(
            ["vmstat", "1", "2"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 4:
            # Get the last line which has the actual values
            last_line = lines[-1].split()
            if len(last_line) >= 15:
                # vmstat format: us sy id wa st
                # We want 100 - idle percentage
                idle = int(last_line[14])  # idle percentage
                cpu_usage = 100 - idle
                return f"{cpu_usage}%"
        
        # Fallback to simpler method
        with open("/proc/loadavg", "r") as f:
            load = f.read().split()[0]
            # Convert load average to rough percentage (load * 100 / cores)
            import os
            cores = os.cpu_count() or 1
            cpu_percent = min(100, int(float(load) * 100 / cores))
            return f"{cpu_percent}%"
        
    except:
        return "N/A"

def get_memory_usage():
    """Get memory usage"""
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        
        mem_total = 0
        mem_available = 0
        
        for line in lines:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1]) / 1024 / 1024  # Convert to GB
            elif line.startswith("MemAvailable:"):
                mem_available = int(line.split()[1]) / 1024 / 1024  # Convert to GB
        
        if mem_total > 0:
            mem_used = mem_total - mem_available
            return f"{mem_used:.1f}G"
        
        return "N/A"
    except:
        return "N/A"

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "LG3D"
