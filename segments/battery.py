def add_battery_segment():
    CAP_FILE = '/sys/class/power_supply/BAT0/capacity'
    STATUS_FILE = '/sys/class/power_supply/BAT0/status'
    LOW_BATTERY_THRESHOLD = 20
    
    f = open(CAP_FILE)
    cap = f.read().strip()
    f.close()
    
    f = open(STATUS_FILE)
    status = f.read().strip()
    f.close()
    
    if status == 'Charging':
        pwr = u' \u21ea '
    else:
        pwr = ' '
    
    if int(cap) < LOW_BATTERY_THRESHOLD:
        bg = Color.BATTERY_LOW_BG
        fg = Color.BATTERY_LOW_FG
    else:
        bg = Color.BATTERY_NORMAL_BG
        fg = Color.BATTERY_NORMAL_FG
    
    powerline.append(' ' + cap + '%' + pwr, fg, bg)

add_battery_segment()
