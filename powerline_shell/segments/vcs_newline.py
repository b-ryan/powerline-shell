import subprocess
from ..utils import RepoStats, ThreadedSegment, get_git_subprocess_env, warn


def get_vcs_dir():
    return_code = subprocess.Popen("git status", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    return_code.communicate()[0].strip()   # Blocks until 'git status' completes execution
    return return_code.returncode


class Segment(ThreadedSegment):
    def run(self):
        self.in_vcs_dir = get_vcs_dir()

    def add_to_powerline(self):
        self.join()
        if self.in_vcs_dir:
            return
        if self.powerline.args.shell == "tcsh":
            warn("newline segment not supported for tcsh (yet?)")
            return
        if self.powerline.segment_conf("vcs", "newline"):
            self.powerline.append("\n",
                                self.powerline.theme.RESET,
                                self.powerline.theme.RESET,
                                separator="")

