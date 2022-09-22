import os
import re
import subprocess
import platform
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):

    def run(self):
        self.num_jobs = 0
        system = platform.system()
        if system.startswith("CYGWIN") or system.startswith("MINGW"):
            # cygwin ps is a special snowflake...
            output_proc = subprocess.Popen(["ps", "-af"], stdout=subprocess.PIPE)
            output = [int(l.split()[2].strip()) for l in output_proc.communicate()[0].decode("utf-8").splitlines()[1:]]
            self.num_jobs = output.count(os.getppid()) - 1
        else:
            # The following logic was tested on:
            # - fish, version 3.3.1
            # - GNU bash, version 5.1.16(1)-release (x86_64-pc-linux-gnu)
            # - zsh 5.8.1 (x86_64-ubuntu-linux-gnu)
            # If you change the behavior to account for another shell's
            # behavior, please provide details of the shell version you tested
            # on in this comment.
            output_proc = subprocess.Popen(["ps", "-a", "-o", "ppid"], stdout=subprocess.PIPE)
            output = output_proc.communicate()[0].decode("utf-8")
            self.num_jobs = len(re.findall(str(os.getppid()), output)) - 1

    def add_to_powerline(self):
        self.join()
        if self.num_jobs > 0:
            self.powerline.append(" %d " % self.num_jobs,
                                  self.powerline.theme.JOBS_FG,
                                  self.powerline.theme.JOBS_BG)
