import subprocess
import re

def add_uptime_segment(powerline):
    try:
        output = subprocess.check_output(['uptime'], stderr=subprocess.STDOUT)
        raw_uptime = re.search('(?<=up).+(?=,\s+\d+\s+user)', output).group(0)
        day_search = re.search('\d+(?=\s+day)', output)
        days = '' if not day_search else '%sd ' % day_search.group(0)
        hour_search =  re.search('\d{1,2}(?=\:)', raw_uptime)
        hours = '' if not hour_search else '%sh ' %  hour_search.group(0)
        minutes =  re.search('(?<=\:)\d{1,2}|\d{1,2}(?=\s+min)', raw_uptime).group(0)
        uptime = u' %s%s%sm \u2191 ' % (days, hours, minutes)
        powerline.append(uptime, Color.CWD_FG, Color.PATH_BG)
    except OSError:
        return
