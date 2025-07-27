#!/bin/bash
echo -e "Power Off\nReboot\nLogout\nLock\nSleep" | \
rofi -dmenu -p "" -theme-str '
    window {
        location: north;
        anchor: north;
        y-offset: -32px;
        width: 100%;
        background-color: #2a343960;
        border: 0;
        border-radius: 0;
    }
    inputbar {
        visible: false;
    }
    listview {
        orientation: horizontal;
        lines: 1;
        spacing: 0;
        margin: 0;
        padding: 0;
    }
    element {
        padding: 8px 16px;
        background-color: transparent;
        text-color: #e0e0e0;
        border-radius: 0;
    }
    element selected {
        background-color: #5e7c8a;
        text-color: #ffffff;
    }' | \
while read choice; do
    case $choice in
        "Power Off") systemctl poweroff ;;
        "Reboot") systemctl reboot ;;
        "Logout") qtile cmd-obj -o cmd -f shutdown ;;
        "Lock") dm-tool lock ;;
	"Sleep") systemctl sleep;;
    esac
done
