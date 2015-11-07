def add_battery_segment():
    f = open('/sys/class/power_supply/BAT0/capacity')
    cap = f.read().strip()
    f.close()
    
    f = open('/sys/class/power_supply/BAT0/status')
    status = f.read().strip()
    f.close()
    
    if status == 'Charging':
        pwr = u' \u21ea '
    else:
        pwr = ' '
    
    if int(cap) > 20:
        bg = Color.HOME_BG
    else:
        bg = Color.READONLY_BG
    
    powerline.append(' ' + cap + '%' + pwr, Color.HOME_FG, bg)

add_battery_segment()
