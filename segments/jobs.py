import os
import re
import subprocess

def add_jobs_segment():
    pppid_proc = subprocess.Popen(['ps', '-p', str(os.getppid()), '-oppid='],
                                  stdout=subprocess.PIPE)
    pppid = pppid_proc.communicate()[0].decode("utf-8").strip()

    output_proc = subprocess.Popen(['ps', '-a', '-o', 'ppid'],
                                   stdout=subprocess.PIPE)
    output = output_proc.communicate()[0].decode("utf-8")

    num_jobs = len(re.findall(str(pppid), output)) - 1

    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

add_jobs_segment()
