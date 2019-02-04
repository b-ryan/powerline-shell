import os
import re
import subprocess
import platform
import sys
try:
    from shutil import which
except ImportError:
    from distutils.spawn import find_executable as which  # EXE is uppercased
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        self.num_jobs = 0
        if platform.system().startswith('CYGWIN') or \
            platform.system().startswith('MSYS') or \
            (platform.system() == 'Windows' and '\\usr\\bin\ps' in (which('ps') or '')):
            # cygwin ps (and msys) is a special snowflake...
            output_proc = subprocess.Popen(['ps', '-af'], stdout=subprocess.PIPE)
            output = map(lambda l: int(l.split()[2].strip()),
                output_proc.communicate()[0].decode("utf-8").splitlines()[1:])
            if sys.version_info[0] < 3:
                self.num_jobs = output.count(os.getppid()) - 1
            else:
                self.num_jobs = list(output).count(os.getppid()) - 1
        else:
            pppid_proc = subprocess.Popen(['ps', '-p', str(os.getppid()), '-oppid='],
                                          stdout=subprocess.PIPE)
            pppid = pppid_proc.communicate()[0].decode("utf-8").strip()
            output_proc = subprocess.Popen(['ps', '-a', '-o', 'ppid'],
                                           stdout=subprocess.PIPE)
            output = output_proc.communicate()[0].decode("utf-8")
            self.num_jobs = len(re.findall(str(pppid), output)) - 1

    def add_to_powerline(self):
        self.join()
        if self.num_jobs > 0:
            self.powerline.append(' %d ' % self.num_jobs,
                                  self.powerline.theme.JOBS_FG,
                                  self.powerline.theme.JOBS_BG)
