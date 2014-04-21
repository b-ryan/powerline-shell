import subprocess
import re

# uptime output samples
# 1h:   00:00:00 up 1:00,  2 users,  load average: 0,00, 0,00, 0,00             
# 10+h: 00:00:00 up 10:00,  2 users,  load average: 0,00, 0,00, 0,00            
# 1+d:  00:00:00 up 1 days, 1:00,  2 users,  load average: 0,00, 0,00, 0,00     
# 9+d:  00:00:00 up 12 days, 1:00,  2 users,  load average: 0,00, 0,00, 0,00    
# mac:  00:00:00 up 233 day(s), 10:00,  2 users,  load average: 0,00, 0,00, 0,00

def add_uptime_segment():
    try:
        output = subprocess.check_output(['uptime'], stderr=subprocess.STDOUT)
        day_search = re.search('\d+(?=\s+day)', output)
        days = '' if not day_search else '%sd ' % day_search.group(0)
        time =  re.search('\d{1,2}\:\d{1,2}(?=,)', output).group(0)
        uptime = u' %s%s ↑ ' % (days, time)
        powerline.append(uptime, Color.CWD_FG, Color.PATH_BG)
    except OSError:
        return

add_uptime_segment()