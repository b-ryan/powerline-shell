import os
from stat import *

def add_jobs_segment():

    myppid = os.getppid()
    CountJobs = {}
    ProcessPid = -1

    for f in os.listdir('/proc'):
        pathname = os.path.join('/proc', f)
        fstat = os.stat(pathname)

        if fstat.st_uid != os.getuid():
            continue

        if S_ISDIR(fstat.st_mode):
            statfile = os.path.join(pathname, 'stat')
            if os.path.isfile(statfile):
                with open(statfile) as f:
                    statline = f.readline()
                    fields   = statline.split()
                    if len(fields) >= 3:
                        process_pid  = fields[0]
                        process_ppid = fields[3]

                        if process_pid == str(myppid):
                           ProcessPid = process_ppid

                        if CountJobs.has_key(process_ppid):
                           CountJobs[process_ppid] += 1
                        else:
                           CountJobs[process_ppid]  = 1

    num_jobs = CountJobs[str(ProcessPid)] - 1
    if num_jobs > 0:
        powerline.append(' %d ' % num_jobs, Color.JOBS_FG, Color.JOBS_BG)

add_jobs_segment()
