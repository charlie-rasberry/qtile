# Backend and blur effects
backend = "glx";
blur-method = "dual_kawase";
blur-strength = 10;
blur-background = true;

# Window transparency
inactive-opacity = 0.85;
active-opacity = 0.95;
frame-opacity = 0.9;

# Shadows (for depth)
shadow = true;
shadow-radius = 20;
shadow-opacity = 0.3;
shadow-offset-x = -5;
shadow-offset-y = -5;

# Rounded corners
corner-radius = 4;
round-borders = 1;
rounded-corners-exclude = [
  "window_type = 'dock'",
  "window_type = 'desktop'",
  "class_g = 'Polybar'",
  "class_g = 'Rofi'"
];
round-borders-exclude = [
  "class_g = 'Polybar'"
];

# Performance optimizations
vsync = true;
dbe = false;
glx-no-stencil = true;
glx-no-rebind-pixmap = true;
use-damage = true;

# Window type exclusions for blur/effects
blur-background-exclude = [
  "window_type = 'dock'",
  "window_type = 'desktop'",
  "class_g = 'Conky'",
  "class_g ?= 'Notify-osd'",
  "class_g = 'Cairo-clock'",
  "_GTK_FRAME_EXTENTS@:c"
];

shadow-exclude = [
  "name = 'Notification'",
  "class_g = 'Conky'",
  "class_g ?= 'Notify-osd'",
  "class_g = 'Cairo-clock'",
  "_GTK_FRAME_EXTENTS@:c"
];
