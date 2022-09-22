import os
import re
import subprocess
import platform
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):

    def pidInfo(self, pid, tag):
        '''
        run a ps and get some data from it
        pid process to query
        tag -o property in the ps command to query for
        return the value from ps
        '''
        ppid = str(pid)
        proc = subprocess.Popen(['ps', '-p', ppid, '-o%s=' % tag],
            stdout=subprocess.PIPE)
        info = proc.communicate()[0].decode("utf-8").strip()
        return info

    def run(self):
        self.num_jobs = 0
        if platform.system().startswith('CYGWIN'):
            # cygwin ps is a special snowflake...
            output_proc = subprocess.Popen(['ps', '-af'], stdout=subprocess.PIPE)
            output = map(lambda l: int(l.split()[2].strip()),
                output_proc.communicate()[0].decode("utf-8").splitlines()[1:])
            self.num_jobs = output.count(os.getppid()) - 1
        else:
            parent_command = self.pidInfo(os.getppid(), "command")
            parent_process_id = self.pidInfo(os.getppid(), "ppid")
            
            #fish runs commands in a sub process, so you have to walk up the
            # tree one time to get back to where you were with bash or other
            # such shells
            if parent_command=="fish":
                parent_process_id = self.pidInfo(parent_process_id, "ppid")
            
            output_proc = subprocess.Popen(['ps', '-a', '-o', 'ppid'], stdout=subprocess.PIPE)
            output = output_proc.communicate()[0].decode("utf-8")
            self.num_jobs = len(re.findall(str(parent_process_id), output)) - 1
    def add_to_powerline(self):
        self.join()
        if self.num_jobs > 0:
            self.powerline.append(' %d ' % self.num_jobs,
                                  self.powerline.theme.JOBS_FG,
                                  self.powerline.theme.JOBS_BG)
