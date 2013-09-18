import os
import re
import subprocess

def add_jobs_segment():
    pppid = subprocess.Popen(['ps', '-p', str(os.getppid()), '-oppid='], stdout=subprocess.PIPE).communicate()[0].strip()
    output = subprocess.Popen(['ps', '-a', '-o', 'ppid'], stdout=subprocess.PIPE).communicate()[0]
    num_jobs = len(re.findall(str(pppid), output)) - 1

    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

add_jobs_segment()
